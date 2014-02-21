#!/usr/bin/env python
#____________________________________________________________
#
# make_webpage.py
#
# Script to produce a web page with a summary of
# validation plots
#
# Francisco Yumiceva
# yumiceva@fnal.gov
#
# Fermilab, 2006
#____________________________________________________________


"""
   usage: %prog 
   -w, --webpath = WEB: path to webpage folder
   -c, --cfg     = CFG: configuration file
   -1, --sample1 = SAMPLE1: cfg sample
   -2, --sample2 = SAMPLE2: cfg sample
   -3, --sample3 = SAMPLE3: cfg sample
   -4, --sample4 = SAMPLE4: cfg sample
   -5, --sample5 = SAMPLE5: cfg sample
   -6, --sample6 = SAMPLE6: cfg sample
   -r, --reference = REFERENCE: CMSSW version of reference plots, default is 1.3.1
   -n, --nocompare : do not compare histograms only produce plots. It can be used to create reference plots.
   -p, --plots : just produce plots.
   -l, --logaxis : produce plots with a logarithm Y-axis scale.
"""

# Modules
#____________________________________________________________
import os
import re
import sys
import fpformat
import pwd
import time
import socket, string
import getopt, popen2, fcntl, select, string, glob
import tempfile
import optparse

#from ROOT import gROOT
USAGE = re.compile(r'(?s)\s*usage: (.*?)(\n[ \t]*\n|$)')

def nonzero(self): # will become the nonzero method of optparse.Values
    "True if options were given"
    for v in self.__dict__.itervalues():
        if v is not None: return True
    return False

optparse.Values.__nonzero__ = nonzero # dynamically fix optparse.Values

class ParsingError(Exception): pass

optionstring=""

def exit(msg=""):
    raise SystemExit(msg or optionstring.replace("%prog",sys.argv[0]))

def parse(docstring, arglist=None):
    global optionstring
    optionstring = docstring
    match = USAGE.search(optionstring)
    if not match: raise ParsingError("Cannot find the option string")
    optlines = match.group(1).splitlines()
    try:
        p = optparse.OptionParser(optlines[0])
        for line in optlines[1:]:
            opt, help=line.split(':')[:2]
            short,long=opt.split(',')[:2]
            if '=' in opt:
                action='store'
                long=long.split('=')[0]
            else:
                action='store_true'
            p.add_option(short.strip(),long.strip(),
                         action = action, help = help.strip())
    except (IndexError,ValueError):
        raise ParsingError("Cannot parse the option string correctly")
    return p.parse_args(arglist)


#__________________
def makeNonBlocking(fd):
    fl = fcntl.fcntl(fd, fcntl.F_GETFL)
    try:
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NDELAY)
    except AttributeError:
            fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.FNDELAY)


#__________________
def runCommand(cmd, printout=0, timeout=-1):
    """
    Run command 'cmd'.
    Returns command stdoutput+stderror string on success,
    or None if an error occurred.
    Following recipe on http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52296
    """
    
    child = popen2.Popen3(cmd, 1) # capture stdout and stderr from command
    child.tochild.close()             # don't need to talk to child
    outfile = child.fromchild
    outfd = outfile.fileno()
    errfile = child.childerr
    errfd = errfile.fileno()
    makeNonBlocking(outfd)            # don't deadlock!
    makeNonBlocking(errfd)
    outdata = []
    errdata = []
    outeof = erreof = 0

    if timeout > 0 :
        maxwaittime = time.time() + timeout

    err = -1
    while (timeout == -1 or time.time() < maxwaittime):
        ready = select.select([outfd,errfd],[],[]) # wait for input
        if outfd in ready[0]:
            outchunk = outfile.read()
            if outchunk == '': outeof = 1
            outdata.append(outchunk)
        if errfd in ready[0]:
            errchunk = errfile.read()
            if errchunk == '': erreof = 1
            errdata.append(errchunk)
        if outeof and erreof:
            err = child.wait()
            break
        select.select([],[],[],.1) # give a little time for buffers to fill
    if err == -1:
        # kill the pid
        os.kill (child.pid, 9)
        err = child.wait()

    cmd_out = string.join(outdata,"")
    cmd_err = string.join(errdata,"")

    if err:
        return None

    cmd_out = cmd_out + cmd_err
    return cmd_out

class save_popen2:
	"""This is a deadlock save version of popen2 (no stdin), that returns
	an object with errorlevel,out, and err"""
	def __init__(self,command):
		outfile=tempfile.mktemp()
		errfile=tempfile.mktemp()
		self.errorlevel=os.system("( %s ) > %s 2> %s" %
					  (command,outfile,errfile)) >> 8
		self.out=open(outfile,"r").read()
		self.err=open(errfile,"r").read()
		os.remove(outfile)
		os.remove(errfile)


#__________________
def runCommand2(cmd):
	"""
	
	"""

	child = save_popen2(cmd) # capture stdout and stderr from command
	errfile = child.err
	outfile = child.out

	outfile = outfile + errfile
	
	return outfile


#________________________________________________________________
def get_list_files_ls(prefix,check = ""):

    dir = []
    if os.path.exists(prefix):
	    dir = os.listdir(prefix)
    
    lfiles = []
    for f in dir:
	    
	    if check=="":
		    lfiles.append(f)
	    
	    elif f.find(check)!=-1:
		    lfiles.append(f)
	    
    return lfiles

#________________________________________________________________
if __name__ == "__main__":

    #import optionparse
    option,args = parse(__doc__)
    if not args and not option: exit()

    webpath = ""
    cmssw_reference = "CMSSW_1_3_1"
    
    if option.webpath:
	    webpath = option.webpath
    else:
	    print " you need to provide a path to the webpage folder"
	    optionparse.exit()
    
    if not option.cfg:
	    print " you need to provide at least one cfg file"
	    optionparse.exit()

    cfgfiles = []
    if option.cfg:
	    cfgfiles.append(option.cfg)

    
    if not option.sample1:
	    print " you need to provide at least one dataset cfg file"
	    optionparse.exit()

    datasets = []
    if option.sample1:
	    datasets.append(option.sample1)
    if option.sample2:
	    datasets.append(option.sample2)
    if option.sample3:
	    datasets.append(option.sample3)
    if option.sample4:
	    datasets.append(option.sample4)
    if option.sample5:
	    datasets.append(option.sample5)
    if option.sample6:
	    datasets.append(option.sample6)

    if option.reference:
	    cmssw_reference = option.reference

    if not option.nocompare:
        print "Using reference plots from version "+cmssw_reference
    else:
        print "Comparasion with reference plots will NOT be run."
    

    # check if make_plots.C exits
    #if not os.path.isfile("make_plots.C"):
    #    print "make_plots.C file does not exist in path, will get it from CVS..."
    #    os.system("cvs co -d tmpdir UserCode/Yumiceva/ValidationTools/make_plots.C")
    #    os.system("mv tmpdir/make_plots.C .")
    #    os.system("rm -rf tmpdir")
    

    
    cmssw_version = os.environ['CMSSW_VERSION']
    
    print "Running Release Validation on " + cmssw_version

    #print "Build ROOT macro "
    #gROOT.ProcessLine(".L make_plots.C++")
    
    for icfg in cfgfiles:

	    for isample in datasets:
		    
		    asample = isample.replace(".cfg","")

                    print " Processing " + icfg + " with dataset " + isample

                    #rootfiles = get_list_files_ls("./",suffix)
		    pkg = "RecoVertex"
		    if icfg.find("RecoVertex_PrimaryVertex")!=-1:
			    pkg = "RecoVertex_PrimaryVertex"
			    #pkg = "RecoVertex"
                    
                    if icfg.find("RecoVertex_Tracking")!=-1:
                        pkg = "RecoVertex_Tracking"
                    
		    if icfg.find("RecoB")!=-1:
			    pkg = "RecoB"
		    
                    #suffix = "validation_PrimaryVertex"
                    folder = webpath + "/packages/"+pkg+"/"+cmssw_version+"/"+asample
		    logfilename = cmssw_version + "_"+ pkg + "_" +asample + ".log"
                    if option.plots:
                        logfilename = folder + "/"+cmssw_version + "_"+ pkg + "_" +asample + ".log"

                    
		    try:
                        if option.plots:
                            outputlog = open(logfilename,"a")
                        else:
                            outputlog = open(logfilename,"w")
		    except IOError:
                        print " Error when try to open file " + logfilename
                        sys.exit()
        

                    
                    rootfilename = folder+"/"+cmssw_version+"_"+pkg + "_" +asample + ".root"
		    ref_rootfilename = webpath + "/packages/"+pkg+"/"+cmssw_reference+"/"+asample+"/"+cmssw_reference+"_"+pkg + "_" +asample + ".root"
                    
                    if not option.plots:
                        
                        os.system("cp "+isample+ " the_data.cfg")

                        outputlog.write( runCommand2("cmsRun "+icfg) )
		    
                        if not os.path.exists(folder):
			    os.makedirs(folder)

                        # check outuput file
                        if not os.path.exists(cmssw_version+"_validation.root"):
                            print " Cannot find "+cmssw_version+"_validation.root Check filename output or output from analyzer. Exit now."
                            sys.exit()
                        
                        os.system("mv "+cmssw_version+"_validation.root "+rootfilename)
                    
                    print " now producing plots"

		    # first write a temp file
		    try:
			    tmpbatchroot = open("tmpbatch.C","w")
		    except IOError:
			    print " Error when try to open file tmpbatch.C"
			    sys.exit()

                    outputlog.write(3*"\n")
                    outputlog.write(10*"=")
                    outputlog.write(" Build ROOT macro to produce plots \n")
                    
		    tmpbatchroot.write('''void tmpbatch() {
                    gROOT->SetStyle("Plain");
                    gSystem->Load("libMakePlots.so");
                    MakePlots plot;
		    ''')

                    tmpbatchroot.write("plot.SetFilename(\""+rootfilename+"\");\n")
                    tmpbatchroot.write("plot.SetWebPath(\""+folder+"\");\n")
                    tmpbatchroot.write("plot.SetExtension(\"png\");\n")
                                        
		    if not option.nocompare:
                        tmpbatchroot.write("plot.SetCompare(true);\n")
                        tmpbatchroot.write("plot.SetCompareFilename(\""+ref_rootfilename+"\");\n")

                    if option.logaxis:
                        tmpbatchroot.write("plot.SetLogAxis(true);\n")

                    tmpbatchroot.write("plot.SetReleaseVer(\""+cmssw_version+"\");\n")
                    tmpbatchroot.write("plot.SetCompareVer(\""+cmssw_reference+"\");\n")
                    tmpbatchroot.write("plot.Draw();\n")
                    tmpbatchroot.write("}\n");
                    
                    tmpbatchroot.close()
                    
                    outputlog.write( runCommand2("root -l -b -q tmpbatch.C") )

                    outputlog.write(3*"\n")
                    outputlog.write(10*"=")
                    outputlog.write("\n")
		    #tmpbatchroot.write("}\n")
		    #os.system("root -l -b -q tmpbatch.C")

                    #os.system("mv "+cmssw_version+"_validation.root "+rootfilename)
                    outputlog.close()
                    if not option.plots:
                        os.system("mv "+logfilename+ " " + folder+"/.")
                        print " root and log file moved to " + folder
                    # clean up
                    os.system("rm -f the_data.cfg")   
		    os.system("rm -f tmpbatch.C")
                    

    os.system("rm -f make_plots.C make_plots_C.so")
		    
                    
		    

		    
