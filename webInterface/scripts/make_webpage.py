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


# Modules
#____________________________________________________________
import os
import re
import sys
import fpformat
import pwd
import time
import socket, string
import webpage

# define paths
#____________________________________________________________
mypath = os.getcwd()

pkgpath = ''
try:
    
    pkgpath = os.environ['CMSSW_BASE']+"/../Validation-Tools/webInterface/templates/"

except LookupError:
    
    pkgpath = "/uscms/home/yumiceva/work/Validation-Tools/webInterface/templates/"

os.chdir(pkgpath)

#__________________
def usage():
    print
    print 'Usage: '+sys.argv[0]+' <absolute path to web directory>'
    print 'e.g.: '+sys.argv[0]+' /uscmst1b_scratch/lpc1/cmsroc/yumiceva/validation'
    print
    return 0

# class to hold records for a row
#________________________________________________________________
class RowElement:
    pass


#________________________________________________________________
def write_to_file(output,headfile="process_tac_head.txt"):
     # read header file
     myfile = None
     #headfile = "head.txt"
     try:
         myfile = open(headfile,"r")
     except IOError:
         print " error opening "+ headfile
         sys.exit()

     # write header part
     for myline in myfile:
         output.write(myline)


#________________________________________________________________
def get_list_files_ls(prefix,check = "",onlyplots = False):

    dir = []
    if os.path.exists(prefix):
        dir = os.listdir(prefix)
    
    lfiles = []
    for f in dir:
        if f == ".htaccess":
            continue
        
        if check=="":
            if onlyplots and not f.endswith(".log") and not f.endswith(".root"):
                lfiles.append(f)
            elif not onlyplots:
                lfiles.append(f)
        
        elif f.find(check)!=-1:
            if onlyplots and not f.endswith(".log") and not f.endswith(".root"):
                lfiles.append(f)
            elif not onlyplots:
                lfiles.append(f)
            
    return lfiles

#________________________________________________________________
def latest(mydatelist):
    thelatest = 0
    thelatest_str = ""
    for idate in mydatelist:
        time_sec = time.mktime(time.strptime(idate,"%a %b %d %H:%M:%S %Y")) 
        if (thelatest < time_sec ):
            thelatest = time_sec
            thelatest_str = idate

    return thelatest_str

#________________________________________________________________
def get_dic(variable,filename):
    file = open(filename)
    dic = {}
    for iline in file:
        iline = iline.strip("\n")
        dic[iline] = 1
    return dic

#________________________________________________________________
def find_str_infile(the_str,file):
    result = 0
    file.seek(0,0)
    for iline in file:
        iline = iline.strip("\n")
        if iline == the_str:
            result = 1
            break

    return result
#________________________________________________________________    
def find_str_inlist(the_str,list):
    result = 0
    for item in list:
        if the_str == item:
            result = 1
            break

    return result

#________________________________________________________________
def find_dqm_color(status):
    # result  color  link
    #   -1    white  no
    #    0    red    no
    #    1    orange no
    #    2    orange yes
    #    3    green  yes
    
    result = "white"
    if status==0:
        result = "red"
    if status==1 or status==2:
        result = "orange"
    if status==3:
        result = "green"

    return result

                
#________________________________________________________________
if __name__ == "__main__":


    webpath = ""
    packagespath = "packages"
    defaultpage = ""
    
    if len(sys.argv)==1 or len(sys.argv)>5:
        usage()
        sys.exit()
    if len(sys.argv)==2:
        try:
            webpath = sys.argv[1]
        except ValueError:
            usage()
            sys.exit()

    outputfilelog = webpath+"/make_webpage.log"
        
    print " working path: " + webpath

    print " log file: " + outputfilelog
    
    print " copying base html files to "+ webpath
    os.system("cp -r css "+webpath)
    os.system("cp -r img "+webpath)
    os.system("cp index_head.txt "+webpath)
    os.system("cp index_foot.txt "+webpath)
    os.system("cp header.txt "+webpath)
    
    os.chdir(webpath)

    
    #print "Current path: "+webpath
    #outputfile = "index.html"
    #outputfilelog = outputfile.replace(".html",".log")
    #try:
#        os.system("mv "+outputfilelog+" "+outputfilelog+".old")
 #   except IOError:
#        print ""

    
    try:
        outputlog = open(outputfilelog,"w")
    except IOError:
        print " Error when try to open file " + outputfilelog
        sys.exit()

        
    # redirec output to log file
    sys.stdout = outputlog
    sys.stderr = outputlog
    
    print "\n"
    print "#"*50
    print "Hello, I am :\t\t"+sys.argv[0]
    print "Run in hostname:\t"+socket.gethostname()
    print "Log file:\t\t"+outputfilelog
    print "Start time:\t\t"+time.asctime(time.localtime())
    print "#"*50
    print "\n"
    
        
    
    print "get list of validation packages"
    lpackages = get_list_files_ls(webpath+"/"+packagespath)
    print "total number of packages = " + str(len(lpackages))
    
    lpackages.sort()

    total_list  = {}
    package_list = lpackages
    thepkglist = []
    
    
    for ipkg in lpackages:
        
        print "get list of releases/directories for "+ipkg
        
        ldirectories = get_list_files_ls(webpath+"/"+packagespath+"/"+ipkg,"CMSSW_")
        print "total number of releases= " + str(len(ldirectories))

        ldirectories.sort()
        ldirectories.reverse()
        string_base1 = ipkg
        samples_list = []
        release_map = {}
        
        for idir in ldirectories:

            ## directory needs to have the string "validation"
            #strloc = idir.find("_validation")
            #release = idir[0:strloc]
            release = idir
            
            print "  get list of samples for release " + release
            lsamples = get_list_files_ls(webpath+"/"+packagespath+"/"+ipkg+"/"+idir)
            lsamples.sort()
            print " total number of samples= " + str(len(lsamples))
            plots_map = {}
            string_base2 = string_base1+"_"+release
            
            for isample in lsamples:

                print "    get list of plots in sample " + isample
                ldirplots = get_list_files_ls(webpath+"/"+packagespath+"/"+ipkg+"/"+idir+"/"+isample,"",True)
                ldirplots.sort()
                print "    total number of plots= " + str(len(ldirplots))
                plots_map[isample] = ldirplots
                string = string_base2+"_"+isample
                samples_list.append(string)
                
            
            release_map[release] = plots_map
        
            
        total_list[ipkg] = release_map
        thepkglist.append(samples_list)
    print " processing page"
    webpage.make_index_page(package_list,thepkglist)

    print " processed main page"
   
    for ipkg in total_list:

        print " Package: " + ipkg

        for irel in total_list[ipkg]:

            print "  release: " + irel

            release_map = total_list[ipkg]
            
            for isample in release_map[irel]:
                
                print "    sample: " + isample

                # output file
                outputfile = "index_"+ipkg+"_"+irel+"_"+isample+".html"
        
                if defaultpage=="":
                    defaultpage = outputfile
            
                try:
                    output = open(outputfile+".tmp","w")
                    print "Output is being written to temporal file: "+ outputfile+".tmp"
    
                except IOError:
                    print " error opening "+ outputfile
                    sys.exit()

                # read header file
                myfile = None
                headfile = webpath+"/index_head.txt"
                try:
                    myfile = open(headfile,"r")
                    print "html header file will be extracted from " + headfile
                except IOError:
                    print " error opening "+ headfile
                    sys.exit()
         
                # write header part
                for myline in myfile:
                    output.write(myline)

                print "header done."
             
                # complete header part of page
        
                output.write('''
            
                <!-- content BEGIN -->
                <div class="fedora-corner-tr">&nbsp;</div>
                <div class="fedora-corner-tl">&nbsp;</div>
                <div id="fedora-content">
                
                <div class="article" lang="en">
                <div class="titlepage"><div><div>
                ''')

                apath = "https://cms-btv-pog-validation.web.cern.ch/cms-btv-pog-validation/validation/"
                rootname = irel+"_"+ipkg+"_"+isample+".root"
                logname = rootname.replace(".root",".log")
                output.write("<center><strong>"+ipkg+" "+irel+" "+isample+"</strong></center>")
                #output.write("<center>[<a href=\""+apath+packagespath+"/"+ipkg+"/"+irel+"/"+isample+"/"+rootname+"\">root</a>] [<a href=\""+apath+packagespath+"/"+ipkg+"/"+irel+"/"+isample+"/"+logname+"\">log</a>]</center>")
                # begin table

                output.write('''<table border=\"1\" cellpadding=\"3\" align=\"center\">
                <tbody align=\"center\">
                ''')

                plots_map = release_map[irel]
                rowcount = 0
                colcount = 0
                for iplot in plots_map[isample]:

                    if (colcount%3)==0:
                        output.write("\n<tr>\n")

                    #apath = "http://nippon.fnal.gov/lpc1/cmsroc/yumiceva/CMSSW_1_5_0_pre2/src/Validation/RecoVertex/test/webpage/"
                    apath = "https://cms-btv-pog-validation.web.cern.ch/cms-btv-pog-validation/validation/"
                    aline = " <td><a href=\""+apath+packagespath+"/"+ipkg+"/"+irel+"/"+isample+"/"+iplot+"\">"
                    output.write(aline)
                        #aline = "\" width=\"340\" border=\"0\" alt=\""+iplot+"\">"
                    aline = "<img src=\""+packagespath+"/"+ipkg+"/"+irel+"/"+isample+"/"+iplot+"\" width=\"340\" border=\"0\" alt=\""+iplot+"\"></a>\n"
                    output.write(aline)

            
                    if (rowcount%2)==0 and rowcount!=0:
                        output.write("</tr>\n")
                        rowcount = 0
                    else:
                        rowcount += 1
                    colcount += 1
            
                # end table
                output.write("  </tbody>\n")
                output.write("</table>\n")
                output.write("\n")
    
                # read end file
                myfile = None
                endfile = webpath+"/index_foot.txt"
                try:
                    myfile = open(endfile,"r")
         
                except IOError:
                    print " error opening "+ endfile
                    sys.exit()

                print " footer done."
            
                # write end part
                for myline in myfile:
                    output.write(myline)

                output.close()
                os.system("mv "+outputfile+".tmp "+outputfile)



    # create default soft link
    #os.system("rm -f index.html")
    #os.system("ln -s "+defaultpage+" index.html")
    

