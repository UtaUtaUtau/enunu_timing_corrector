from argparse import ArgumentParser
import os

class Phoneme(): # Phoneme Class
    def __init__(self, start, end, phone):
        self.start = start
        self.end = end
        self.phone = phone
        self.duration = end - start

    @staticmethod
    def from_line(line):
        l = line.strip().split()
        return Phoneme(int(l[0]), int(l[1]), l[2])

    def __eq__(self, other):
        return (self.start == other.start) and (self.end == other.end)

    def __repr__(self):
        return f'{self.start} {self.end} {self.phone}'

    def __str__(self):
        return self.__repr__()

def parse_labels(mono_score, mono_timing):
    '''
    Parses labels and groups phonemes by note by checking the mono score label
    '''
    # Read labels
    score = open(mono_score, encoding='utf8')
    timing = open(mono_timing, encoding='utf8')

    # Prepare list
    score_list = []
    timing_list = []

    # Start reading
    score_line = score.readline()
    timing_line = timing.readline()
    while score_line:
        # Make phoneme class from line
        score_phone = Phoneme.from_line(score_line)
        timing_phone = Phoneme.from_line(timing_line)

        if len(score_list) == 0: # Start edge case
            score_list.append([score_phone])
            timing_list.append([timing_phone])
        elif score_list[-1][-1] == score_phone: # Append to last list if current mono score has the same timing as the first
            score_list[-1].append(score_phone)
            timing_list[-1].append(timing_phone)
        else:
            score_list.append([score_phone])
            timing_list.append([timing_phone])
        
        score_line = score.readline()
        timing_line = timing.readline()

    # Close files
    score.close()
    timing.close()

    # Return both lists
    return score_list, timing_list

def correct_timing(score_list, timing_list, vowels):
    '''
    Correct timing by referencing durations from timing list.
    The score list will be the corrected version of the timing list.
    '''
    for i in range(len(score_list)): # Initial correct (note by note)
        score = score_list[i]
        timing = timing_list[i]
        if len(score) != 1: # No need to correct notes with only one phoneme inside
            # Find vowel
            vowel_idx = 0
            for j in range(len(score)):
                if score[j].phone in vowels:
                    vowel_idx = j
                    break

            # Correct onset positioning
            for j in range(vowel_idx-1, -1, -1):
                score[j].end = score[j+1].start
                score[j].start = score[j].end - timing[j].duration
                score[j].duration = timing[j].duration

            # Correct coda
            coda_len = 0
            for j in range(vowel_idx+1, len(score)):
                # Accumulate coda length...
                coda_len += timing[j].duration

            # ...and subtract to vowel
            score[vowel_idx].duration -= coda_len
            score[vowel_idx].end -= coda_len

            # Correct coda positioning
            for j in range(vowel_idx+1, len(score)):
                score[j].start = score[j-1].end
                score[j].end = score[j].start + timing[j].duration
                score[j].duration = timing[j].duration

    for i in range(1, len(score_list)): # Overlapping label correct
        curr = score_list[i]
        prev = score_list[i-1]
        if curr[0].start != prev[-1].end: # If overlapping
            # Correct end of previous note
            prev[-1].end = curr[0].start
            if len(prev) == 1:
                # Skip if previous note only has one phoneme
                continue

            # Find first vowel
            vowel_idx = 0
            for j in range(len(prev)):
                if prev[j].phone in vowels:
                    vowel_idx = j
                    break

            if vowel_idx == len(prev)-1:
                # Skip if first vowel index is the last index
                continue
                
            # Correct coda positioning
            prev[-1].start = curr[0].start - prev[-1].duration
            for j in range(len(prev)-2, vowel_idx-1, -1):
                prev[j].end = prev[j+1].start
                if j != vowel_idx:
                    prev[j].start = prev[j].end - prev[j].duration
                    
    for i in range(len(score_list)-1, 0, -1): # Negative duration correct
        curr = score_list[i]
        prev = score_list[i-1]
        for j in range(len(curr)-1, -1, -1):
            if curr[j].end - curr[j].start <= 0:
                curr[j].start = curr[j].end - 10000
                if j > 0:
                    curr[j-1].end = curr[j].start
                else:
                    prev[-1].end = curr[j].start
            
if __name__ == '__main__':
    parser = ArgumentParser(description='Corrects timing from mono score and generated timing')
    parser.add_argument('--mono_score', help='The mono score of the output')
    parser.add_argument('--mono_timing', help='The processed timing')

    args, _ = parser.parse_known_args()

    vowels = open('vowels.txt', encoding='utf8').read().split(',')
    #print(vowels)

    score_list, timing_list = parse_labels(args.mono_score, args.mono_timing)
    #print(score_list[0:5])
    #print(timing_list[0:5])

##    with open("D:\\voice\\Deshi_AI_---\\timing_corrector\\raw.lab", 'w', encoding='utf8', newline='\n') as f:
##        for i in timing_list:
##            for j in i:
##                f.write(str(j) + f' {j.end - j.start}' + '\n')
    
    correct_timing(score_list, timing_list, vowels)
    #print(score_list[0:5])
    #print(timing_list[0:5])

    #os.rename(args.mono_timing, args.mono_timing + '.bak')

    # Write corrected label to timing
    with open(args.mono_timing, 'w', encoding='utf8', newline='\n') as f:
        for i in score_list:
            for j in i:
                f.write(str(j) + '\n')

##    with open("D:\\voice\\Deshi_AI_---\\timing_corrector\\processed.lab", 'w', encoding='utf8', newline='\n') as f:
##        for i in score_list:
##            for j in i:
##                f.write(str(j) + f' {j.end - j.start}' + '\n')
