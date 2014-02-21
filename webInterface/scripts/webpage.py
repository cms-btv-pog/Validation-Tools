# webpage.py
#
# Script to produce the index web page with a summary of
# validation plots
#____________________________________________________________
# Modules
#____________________________________________________________
import os
import sys


# function to get the main page
#_____________________________________________________________
def make_index_page(package_list,thepkglist):

    	 myfile = "index.html"
         try:
		 outfile = open(myfile,"w")
	 except IOError:
		 print " error opening "+ myfile
		 sys.exit()


    	 myheader = "header.txt"
         try:
		 infile = open(myheader,"r")
                 print "html header file will be extracted from " + myheader
	 except IOError:
		 print " error opening "+ myheader
		 sys.exit()
	 for myline in infile:
		 outfile.write(myline)

         print "header done."


         i = 0
         for pkg in package_list :
             outfile.write('''<form  method="post"onReset="return ()" >
             <b><font color=blue size="4">''' + pkg +'''</font></b>
             <select name="choice" size="1"><option value="" >Select Sample
             </option>''')

             for lpkg in thepkglist[i]:         
                 outfile.write('''<option value ="https://cms-btag-validation.web.cern.ch/cms-btag-validation/validation/index_'''+lpkg+'''.html">'''+ lpkg + '''</option>''')
#           outfile.write('''<option value ="http://nippon.fnal.gov:8888/lpc1/cmsroc/yumiceva/validation/index_'''+lpkg+'''.html">'''+ lpkg + '''</option>''')
      
                 continue
             
             outfile.write('''</select><input type="button" value="Find" onClick="jump(this.form)">
         <input type="RESET" value="Reset"></form>
         <BR>''')
             i = i+1
         outfile.write('''       

         </html>
         ''')
         outfile.close()
