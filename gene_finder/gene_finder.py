# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:24:42 2014

@author: Sean Carter (SeanCCarter on github)

"""

# you may find it useful to import these variables (although you are not required to use them)
from amino_acids import aa, codons, aa_table
import random
from load import load_seq

def shuffle_string(s):
    """ Shuffles the characters in the input string
        NOTE: this is a helper function, you do not have to modify this in any way """
    return ''.join(random.sample(s,len(s)))

### YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('T')
    'A'
    >>> get_complement('G')
    'C'
    """
    compliments = {'A':'T', 'T':'A', 'C':'G','G':'C'}
    return compliments[nucleotide]

def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence
    
        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    #Tests are sufficient. There's only so much that this could mess up
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    """
    compliment = ''
    for letter in dna:
        compliment += get_complement(letter)
    return compliment[::-1] #returns the reversed version of the compliment with slicing

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start codon and returns
        the sequence up to but not including the first in frame stop codon.  If there
        is no in frame stop codon, returns the whole string.
        
        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    """
    ORF = ''
    #The tests do a pretty good job. No point in testing what happens when it gets one that isn't
    #and ORF, because that's not the point of the function.
    while dna[0:3] not in {'TAG', 'TAA', 'TGA'} and dna:
        ORF += dna[0:3]
        dna = dna[3:]
    return ORF

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence and returns
        them as a list.  This function should only find ORFs that are in the default
        frame of the sequence (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("GGCAATGATGGCATCATGAGTATAG")
    ['ATGAGTATAG']
    >>> find_all_ORFs_oneframe("GGCATGATGGCATCATGAGTATAGAGTA")
    ['ATGATGGCATCA']
    >>> find_all_ORFs_oneframe("AATGGC")
    []
    """
    #The two extra tests above were added, to make sure that both the recursion and the potential for letters
    #to be something other than an ORF at the beginning of the sequence. Also, extraneous letters at the back
    ORFs = []
    while dna[0:3] != 'ATG' and len(dna) > 3:
        dna = dna[3:]

    if len(dna) <= 3 and dna != 'ATG':
        return ORFs
    elif len(dna) > 3:
        ORFs.append(rest_of_ORF(dna))
        dna = dna[len(ORFs[-1]):]
        ORFs += find_all_ORFs_oneframe(dna)        
        return ORFs
    else:
        ORFs.append(dna)
        return ORFs

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in all 3
        possible frames and returns them as a list.  By non-nested we mean that if an
        ORF occurs entirely within another ORF and they are both in the same frame,
        it should not be included in the returned list of ORFs.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs

    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    >>> find_all_ORFs("ATGATGCATGAATGTAG")
    ['ATGATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    # Added one test, to check and make sure that it doesn't find nested ORFs
    ORFs = []
    for i in range(3):
        ORFs += find_all_ORFs_oneframe(dna[i:])
    return ORFs

def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.
        
        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    #This test does check to see whether it can get it from both strands
    ORFs = find_all_ORFs(dna) + find_all_ORFs(get_reverse_complement(dna))
    return ORFs


def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    >>> longest_ORF("ATGCGAATGTAGCATCAAAATGCGAATG")
    'ATGCTACATTCGCAT'
    """
    #This function will only return the first ORF if there are two longest ones that
    #are the same size. However, we are only using it to find its length, so that doesn't
    #matter here
    return max(find_all_ORFs_both_strands(dna), key = len)
    


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence
        
        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    ORFlens = []
    while num_trials:
        dna = shuffle_string(dna)
        ORFlens.append(len(longest_ORF(dna)))
        num_trials -= 1
    return max(ORFlens)

def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).
        
        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
        >>> coding_strand_to_AA("CCCGCTTT")
        'PA'
    """
    #Added test to check whether it can handle a case without a start codon
    codons = ''
    while len(dna) >= 3: #Just in case the strand isn't quite divisible by 3
        codons += aa_table[dna[0:3]]
        dna = dna[3:]
    return codons

def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna
        
        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    #Given its randomness, there isn't a good way to test it within the doctest framework
    #The project will break if there are no open reading frames
    threshold = longest_ORF_noncoding(dna, 1500)
    return [ORF for ORF in find_all_ORFs_both_strands(dna) if len(ORF) >= threshold]

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    from load import load_seq
    dna = load_seq("./data/X73525.fa")
    ORFs = gene_finder(dna)
    proteins = [coding_strand_to_AA(orf) for orf in ORFs]
    print proteins
