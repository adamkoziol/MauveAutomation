#! /usr/bin/env python
__author__ = 'akoziol'

import os, glob, shutil, errno, re

# path = os.getcwd()
path = "/media/nas/akoziol/Collaborations/Austin/QC_OptimisationTimeTrial/2014-12-09"
# path = "/media/nas/akoziol/Pipeline_development/ePFGE/2014-11-28"
# path = "/media/nas/akoziol/Pipeline_development/ePFGE/2014-11-21/Listeria"
os.chdir(path)
folders = glob.glob("*")


def make_path(inPath):
    """from: http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary \
    does what is indicated by the URL"""
    try:
        os.makedirs(inPath)
        # os.chmod(inPath, 0777)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def automateMauve():
    """Automates mauve"""
    for folder in folders:
        genomeFile = ''
        count = 0
        if os.path.isdir(folder):
            if folder == "pseudomolecules":
                pass
            else:
                # print folder
                os.chdir("%s/%s" % (path, folder))
                #java -Xmx500m -cp Mauve.jar org.gel.mauve.contigs.ContigOrderer -output results_dir -ref reference.gbk -draft draft.fasta
                #java -Xmx500m -cp /home/blais/Bioinformatics/mauve_2.3.1/Mauve/Mauve.jar
                contigs = glob.glob("*_filteredAssembled.fasta")
                if contigs:
                    contigsFA = contigs[0].replace(".fasta", ".fa")
                    shutil.move(contigs[0], contigsFA)
                if not os.path.isdir("%s/%s/MauveResults" % (path, folder)):
                    mauveCommand = "java -Xmx500m -cp /home/blais/Bioinformatics/mauve_2.3.1/Mauve.jar org.gel.mauve.contigs.ContigOrderer " \
                               "-output MauveResults -ref *.fasta -draft %s" % contigsFA
                    os.system(mauveCommand)
                os.chdir("%s/%s/MauveResults" % (path, folder))
                # os.system("ls -larth")
                # os.system("pwd")
                alignments = glob.glob("*")
                sortedAlignments = sorted(alignments)
                alignmentFolder = sortedAlignments[-1]
                os.chdir("%s/%s/MauveResults/%s" % (path, folder, alignmentFolder))
                if not os.path.isfile("%s/%s/MauveResults/%s/%s_pseudomolecule.fa" % (path, folder, alignmentFolder, folder)):
                    orderedContigs = glob.glob("*.fas")
                    # os.chdir("%s/%s" % (path, folder))
                    with open(orderedContigs[0], "r") as contigFile:
                        for line in contigFile:
                            if line.startswith(">"):
                                pass
                            else:
                                genomeFile += line.rstrip()
                    print folder, len(genomeFile)
                    with open("%s/%s/%s_pseudomolecule.fa" % (path, folder, folder), "wb") as pseudomolecule:
                        pseudomolecule.write(">%s_pseudomolecule\n" % folder)
                        for pos in genomeFile:
                            if count < 60:
                                pseudomolecule.write(pos.upper())
                                count += 1
                            else:
                                pseudomolecule.write("\n")
                                pseudomolecule.write(pos.upper())
                                count = 1
                        pseudomolecule.write("\n")
                make_path("%s/pseudomolecules" % path)
                shutil.copy("%s/%s/%s_pseudomolecule.fa" % (path, folder, folder), "%s/pseudomolecules/%s_pseudomolecule.fa" % (path, folder))
                del genomeFile
                ####
                interest = False
                genomeString = ""
                count1 = 0
                alignmentFile = [files for files in os.listdir("%s/%s/MauveResults/%s" % (path, folder, alignmentFolder))
                                 if re.search('alignment\d$', files)]
                with open(alignmentFile[0], "r") as alignment:
                    for line in alignment:
                       if re.search("> 2", line):
                           interest = True
                       elif re.search("=", line):
                           interest = False
                       elif interest is True:
                           genomeString += line.rstrip()
                with open("%s/%s/%s_scaffoldPseudomolecule.fa" % (path, folder, folder), "wb") as pseudomoleculeScaff:
                    pseudomoleculeScaff.write(">%s_scaffoldedPseudomolecule\n" % folder)
                    for pos in genomeString:
                        if count1 < 60:
                            pseudomoleculeScaff.write(pos.upper().replace("-", "N"))
                            count1 += 1
                        else:
                            pseudomoleculeScaff.write("\n")
                            pseudomoleculeScaff.write(pos.upper().replace("-", "N"))
                            count1 = 1
                    pseudomoleculeScaff.write("\n")
                shutil.copy("%s/%s/%s_scaffoldPseudomolecule.fa" % (path, folder, folder),
                            "%s/pseudomolecules/%s_scaffoldPseudomolecule.fa" % (path, folder))
        os.chdir(path)

automateMauve()