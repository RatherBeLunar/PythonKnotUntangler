

length=0
auto=1

#knot=[1, -2, 3, -4, 5, -6, 4, -7, 2, -1, 6, -5, 7, -3]
#knot=[1, -2, 3, -4, 5, -6, 7, -5, 2, -1, 8, -7, 6, -8, 4, -3]
#knot=[1, -2, 3, -4, 5, -6, 7, -8, 6, -1, 2, -5, 9, -7, 8, -9, 4, -3]
#knot=[1, 2, -3, 4, 5, -6, 2, 1, -6, -3, -7, 8, 9, 10, 8, -11, -12, 9, 10, 5, 4, -7, -11, -12]

#knot=[1,-2,-3,4,5,-6,-7,8,-9,3,-10,-5,6,-1,2,10,-4,7,-8,9]
#knot=[1,-2,-3,4,5,-6,7,-5,2,-8,-9,10,-4,3,8,-1,6,-7,-10,9]
#knot.reverse()

#[1, -2, 3, -4, 5, 6, -7, 8, -9, -5, 10, -1, 2, -3, -8, 9, 4, -10, -6, 7]
#[1, -2, 3, -4, 5, 6, -7, 8, -9, -5, 10, -1, 2, 7, -6, -10, 4, 9, -8, -3]


def checkValid(testKnot):
    for idx1 in range(len(testKnot)):
        idx2 = testKnot.index(-testKnot[idx1])
        if abs(idx2 - idx1)%2==0:
            return False
    return True


def separate(testKnot,signs):
    firstInst=[]
    secInst=[]
    
    doSeparate=0
    
    for item in testKnot:
        if -item not in testKnot:
            doSeparate=1
    
    if doSeparate==1:
        #Scan all numbers in knot
        for i in range(len(testKnot)):
            #If a number (pos/neg irrelevant) has not occurred before,
            if testKnot[i] not in firstInst and -testKnot[i] not in firstInst:
                #note that it has now occurred
                firstInst.append(testKnot[i])
                secInst.append(0)
            else:
                #If the number has been seen before, note that as well
                secInst.append(testKnot[i])
                firstInst.append(0)
        
        #For every second instance of a number in knot, 
        for i in range(len(secInst)):
            if secInst[i]!=0:
                #add its sign value to the signs list
                signs.append(secInst[i]/abs(secInst[i]))
            else:
                signs.append(0)    
        
        
        #If a number appears twice with the same sign,
        for i in range(len(testKnot)):
            if secInst[i]!=0 and secInst[i] in firstInst:
                #Negate the second instance to get the name into non-extended form
                testKnot[i]=-secInst[i]
        #If no second instances need to be changed,
        #The input is already in normal Gauss Code
    else:
        for i in range(len(testKnot)):
            signs.append(0)
        

#Re-joins the split Gauss code at the end of the program
#Again, if the input was standard Gauss Code, this function does not affect the outcome
def join(testKnot,signs):
    for i in range(len(testKnot)):
        if signs[i]!=0:
            testKnot[i]=abs(testKnot[i])*signs[i]
    signs=[]
            

#takes a list and "rotates" it to the right.
#The last digit gets put in front of the first
#[1,2,3,4] becomes [4,1,2,3]
def shift(testKnot,signs):
    testKnot.insert(0,testKnot[-1])
    signs.insert(0,signs[-1])
    testKnot.pop(-1)  
    signs.pop(-1)
    

            

#Effectively flips the knot
#Does not physically change the knot
def flip(testKnot):
    for x in range(len(testKnot)):
        testKnot[x]=-testKnot[x]
    


#Gives the mirror of the knot
#Physically changes the knot
def mirror(signs):
    for x in range(len(signs)):
        signs[x]=-signs[x]



#Reduces the numbers in the name of a knot to the range of -n to n
#for a knot with n crossings
def reduceName(testKnot,signs):
    #redOrdered stores all the numbers from -n to n
    redOrdered=[]
    #ordered stores and sorts all the values in knot
    ordered=[]
    #reduced is where the final reduced name is created
    reduced=[]
    
    #this is doing what you'd expect ordered = knot to do,
    #but for some reason, the assignment operator leaves the two interconnected
    for i in range(len(testKnot)):
        ordered.append(testKnot[i])
    
    for i in range(len(testKnot)+1):
        redOrdered.append(i-len(testKnot)/2)
        reduced.append(0)
    redOrdered.remove(0)
    reduced.remove(0)
    ordered.sort()
    #redOrdered and ordered are now as they should be for the reducing process
    #and reduced is a list of appropriate length, full of placeholder zeros
    for i in range(len(testKnot)):
        #take a number from ordered
        #find where it is in knot
        #and for that same index in reduced
        #assign it the reduced value from redOrdered
        reduced[testKnot.index(ordered[i])]=redOrdered[i]
    
    #Reassign reduced to knot
    for i in range(len(testKnot)):
        testKnot[i]=reduced[i]

    


#Finds the longest segment of numbers in the name
#That has no numbers repeated within the segment
#And sets that segment to the beginning of the list
def lineUp(testKnot,signs,seg):

    while testKnot[0]!=seg[0]:
        shift(testKnot,signs)

    if testKnot[0]<0:
        flip(testKnot)

                    
    
    #The max length of a non-repeated segment is equal to the number of crossings
    #But it can also be less than that
    #If there is no valid non-repeated segment of a certain length, reduce the length
    #and try again




#Performs legal number switching of the name
#Such that the name begins with +1, and every number following is sequential
#until a number must be repeated
def numberSwap(testKnot,signs):
    global length
    #temp holds the numbers being switched while the switching occurs
    temp=[]
    for i in range(len(testKnot)):
        temp.append(0)
    for i in range(len(testKnot)):
        #If a number is already sequential as we want it to be,
        #Then we don't have to switch it
        if abs(testKnot[i])==i+1:
            continue      
        #In the case that the selected number is positive
        #And the proposed switch is valid
        if testKnot[i]>0 and (testKnot.index(-testKnot[i])>i):
                #a1 is the selected number
                #a2 is its negative
                a1=testKnot[i]
                a2=-testKnot[i]
                
                #Storing the switches in temp
                
                #Put the sequential values at the locations of a1 and a2
                temp[testKnot.index(a1)]=i+1
                temp[testKnot.index(a2)]=-(i+1)
                
                #Put a1 and a2 at the locations of the sequential values
                temp[testKnot.index(i+1)]=a1
                temp[testKnot.index(-(i+1))]=a2
                
                
                #Apply the switches to knot, remove them from temp
                for j in range(len(testKnot)):
                    if temp[j]!=0:
                        testKnot[j]=temp[j]
                        temp[j]=0
        #In the case that the selected number is negative
        #And the proposd switch is valid
        elif testKnot[i]<0 and (testKnot.index(-testKnot[i])>i):
                #a1 is the selected number
                #a2 is its negative
                a1=testKnot[i]
                a2=-testKnot[i]
                
                #Storing the switches in temp
                
                #Put the sequential values at the locations of a1 and a2
                temp[testKnot.index(a1)]=-(i+1)
                temp[testKnot.index(a2)]=i+1
                
               
                #Put a1 and a2 at the locations of the sequential values
                temp[testKnot.index(-(i+1))]=a1
                temp[testKnot.index(i+1)]=a2
               
                
                #Apply the switches to knot, remove them from temp
                for j in range(len(testKnot)):
                    if temp[j]!=0:
                        testKnot[j]=temp[j]
                        temp[j]=0

        #If there is no valid switch left to be made, then stop
        else:
            break       
    
    


def getAlterSeg(testKnot):
    #longest non-repeating, alternating strand
    seg=[]
    finalSeg=[]
    done=0
    for segLength in range(len(testKnot)/2,0,-1):
        if done==1:
            break
        for i in range(-len(testKnot),0):
            if done==1:
                break
            if i+segLength+1>len(testKnot):
                continue
            elif i<0 and i+segLength+1>0:
                seg=testKnot[i:]+testKnot[:i+segLength+1]
            elif i<0 and i+segLength+1<0:
                seg=testKnot[i:i+segLength+1]
            elif i<0 and i+segLength+1==0:
                seg=testKnot[i:]
            elif i>0:
                seg=testKnot[i:i+segLength+1]
            for j in range(len(seg)):
                if done==1:
                    break
                if seg[j]/abs(seg[j])!=(-1)**j or -seg[j] in seg:
                    for k in range(len(seg)):
                        if done==1:
                            break
                        if seg[k]/abs(seg[k])!=(-1)**(k+1) or -seg[k] in seg:
                            break
                    else:
                        if done==1:
                            break
                        finalSeg=seg
                        done=1
                        break
                    break
            else:
                if done==1:
                    break
                finalSeg=seg
                done=1
                break

    return finalSeg


def getNonAlterSeg(testKnot):
    seg=[]
    finalSeg=[]
    done=0
    for segLength in range(len(testKnot)/2,0,-1):
        if done==1:
            break
        for i in range(-len(testKnot),0):
            if done==1:
                break
            if i+segLength+1>len(testKnot):
                continue
            elif i<0 and i+segLength+1>0:
                seg=testKnot[i:]+testKnot[:i+segLength+1]
            elif i<0 and i+segLength+1<0:
                seg=testKnot[i:i+segLength+1]
            elif i<0 and i+segLength+1==0:
                seg=testKnot[i:]
            elif i>0:
                seg=testKnot[i:i+segLength+1]
            for j in range(len(seg)):
                if done==1:
                    break
                if -seg[j] in seg:
                    for k in range(len(seg)):
                        if done==1:
                            break
                        if -seg[k] in seg:
                            break
                    else:
                        if done==1:
                            break
                        finalSeg=seg
                        done=1
                        break
                    break
            else:
                if done==1:
                    break
                finalSeg=seg
                done=1
                break

    return finalSeg



def changeFormAlter(testKnot,signs):
    auto=1
    #number of crossings
    n=len(testKnot)/2
    #print "alternating"   
    alterSeg=getAlterSeg(testKnot[:])
    whileLoopDone=0
    while len(alterSeg)!=n:
        if whileLoopDone==1:
            break
        sizeLoopDone=0
        for size in range(len(testKnot)/2,0,-1):
            if sizeLoopDone==1:
                break
            tangles=(findTangles(testKnot[:],size))[:]
            iLoopDone=0
            for i in range(len(tangles)):
                if iLoopDone==1:
                    break
                
                move2=transMove2(testKnot[:],signs[:],tangles[i])
                if len(alterSeg)<len(getAlterSeg(move2[0])):
                    testKnot=move2[0]
                    signs=move2[1]
                    alterSeg=getAlterSeg(testKnot[:])
                    if auto==0:
                        print "Translation Move 2 worked"
                        print testKnot
                        print alterSeg
                        raw_input()
                    sizeLoopDone=1
                    iLoopDone=1
                    break
                if len(tangles[i][0])<2:
                    break
                    
                move1=transMove1(testKnot[:],signs[:],tangles[i])
                if len(alterSeg)<len(getAlterSeg(move1[0])):
                    testKnot=move1[0]
                    signs=move1[1]
                    alterSeg=getAlterSeg(testKnot[:])
                    if auto==0:
                        print "Translation Move 1 worked"
                        print testKnot
                        print alterSeg
                        raw_input()
                    sizeLoopDone=1
                    iLoopDone=1
                    break
        
        if sizeLoopDone==0:
            whileLoopDone=1
            break
    
    global length
    length=len(alterSeg)
    return testKnot   
     
def changeFormNonAlter(testKnot,signs):
    
    #number of crossings
    n=len(testKnot)/2
    #print "nonalternating"
    nonAlterSeg=getNonAlterSeg(testKnot[:])
    whileLoopDone=0
    while len(nonAlterSeg)!=n:
        if whileLoopDone==1:
            break
        sizeLoopDone=0
        for size in range(len(testKnot)/2,0,-1):
            if sizeLoopDone==1:
                break
            tangles=(findTangles(testKnot[:],size))[:]
            iLoopDone=0
            for i in range(len(tangles)):
                if iLoopDone==1:
                    break
                
                move2=transMove2(testKnot[:],signs[:],tangles[i]) 
                if len(nonAlterSeg)<len(getNonAlterSeg(move2[1])):
                    testKnot=move2[0]
                    signs=move2[1]
                    nonAlterSeg=getNonAlterSeg(testKnot[:])
                    if auto==0:
                        print "Translation Move 2 worked"
                        print testKnot
                        print nonAlterSeg
                        raw_input()
                    sizeLoopDone=1
                    iLoopDone=1
                    break
                if len(tangles[i][0])<2:
                    break
                
                move1=transMove1(testKnot[:],signs[:],tangles[i])
                if len(nonAlterSeg)<len(getNonAlterSeg(move1[0])):
                    #print testKnot
                    testKnot=move1[0]
                    signs=move1[1]
                    nonAlterSeg=getNonAlterSeg(testKnot[:])
                    if auto==0:
                        print "Translation Move 1 worked"
                        print testKnot
                        print nonAlterSeg
                        raw_input()
                    sizeLoopDone=1
                    iLoopDone=1
                    break
        
        if sizeLoopDone==0:
            whileLoopDone=1
            break
    
    global length
    length=len(nonAlterSeg)
    return testKnot 


def name(testKnot,signs):
    auto=1
    
    if signs==[]:
        separate(testKnot,signs)
        if auto==0:
            print "Separated: ",testKnot
            print "signs: ",signs
            raw_input()
            
            
    if max(testKnot)>len(testKnot)/2:
        reduceName(testKnot,signs)
        if auto==0:
            print "Reduced: ",testKnot
            raw_input()
            
    
    lineUpSeg=getAlterSeg(testKnot)
    if len(getAlterSeg(testKnot))<len(testKnot)/2:
        changeFormAlter(testKnot,signs)
        lineUp(testKnot,signs,getAlterSeg(testKnot))
        if auto==0:
            print "Alternating: ",testKnot
            raw_input()
    
    
    if len(getAlterSeg(testKnot))<len(testKnot)/2:
        changeFormNonAlter(testKnot,signs)
        lineUpSeg=getNonAlterSeg(testKnot)
        if auto==0:
            print "NonAlternating: ",testKnot
    
    lineUp(testKnot,signs,lineUpSeg)
    
    if auto==0:
        print "Shifted: ",testKnot
        raw_input()
        print "Re-numbering..."
    numberSwap(testKnot,signs)
    
    if max(signs)!=0 or min(signs)!=0:
        if auto==0:
            print "Knot: ",testKnot
            raw_input()
            print "Joining..."
            print ""
        join(testKnot,signs)
    
    
    signs=[]
    #print "Final Knot: ",testKnot
    



auto=0



#Finds all the tangles of a given size in the knot
def findTangles(testKnot,size):
    if size==0:
        return
    else:
        #tangles holds a list of all the tangles found
        tangles=[]
        for a in range(-len(testKnot),0):
            idxA=a
            
            #segA finds the first half segment of a tangle
            #There are two segments to a tangle, they complete each others' crossings
            segA=[testKnot[idxA]]
            
            #sizeA regulates the size that segA is allowed to grow to
            sizeA=size
            
            #lensegA is a "virtual" length of segA
            #The actual length of segA cannot be used
            #Because there are cases where a crossing is completed within segA
            #and thus we don't need to look for that crossing in segB
            lensegA=1
            
            #sizeB is a "virtual" size for B which is dependent on how many crossings are completed in segA
            sizeB=size
        
            #create segA
            while lensegA!=sizeA:
                #move to the next index in the knot
                idxA=idxA+1
                
                #Sometimes the function will try to look further than the end of the knot
                #in which case we just stop
                if idxA==len(testKnot)-1:
                    break
                
                #If a crossing completes itself in segA, then segA has more than the given size of crossings
                #So segB doesn't need to contain as many
                #With this, we do not increase the virtual length of segA
                if -testKnot[idxA] in segA:
                    sizeB=sizeB-1
                    segA.append(testKnot[idxA])
                
                #If the crossing is unique, we simply add it, increase the virtual length of segA
                #and continue
                else:
                    segA.append(testKnot[idxA])
                    lensegA=lensegA+1
            
            
            #Now we have a completed segA, and we can create a segB that is "dependent" on segA
            for b in range(-len(testKnot),0):
                idxB=b
                
                #Create an initial segB
                segB=[testKnot[idxB]]
                while len(segB)!=sizeB:
                    #Move to the next index in the knot
                    idxB=idxB+1
                    
                    #if we reach the end of the knot, stop
                    if idxB==len(testKnot)-1:
                        break
                    
                    #Here we can just add items to segB until we complete the size requirement
                    #We're about to test the validity of the segments anyway, so we can be simple here
                    segB.append(testKnot[idxB])
                
                #The way the testing is set up, we assume the tangle is valid until we prove otherwise
                valid=1
                
                for item in segA:
                    #If an item in segA is not completed in segA or segB
                    #or if the item is duplicated in segB
                    if ((-item not in segA) and (-item not in segB)) or (item in segB):
                        #...then the tangle is invalid
                        valid=0
                        break
                if valid==1:
                    #Repeate the same test for segB
                    for item in segB:
                        if ((-item not in segA) and (-item not in segB)) or (item in segA):
                            valid=0
                            break
                    if valid==1:
                        #If we don't have duplicates, we record the tangle in the list
                        if (segB,segA) not in tangles and len(segA)<len(testKnot)/2 and len(segB)<len(testKnot)/2:
                            tangles.append((segA,segB))
                        break
    return tangles



def transMove1(testKnot,signs,tangle):
    done=0
    #We examine a tangle from both sides
    for j in [-1,0]:
        if done==1:
            break
            
        #Name the halves of the tangle
        seg1=tangle[j]
        seg2=tangle[j+1]
        
        #a2,b2,c2,d2 are the 4 crossings on the outside of the tangle
        #A tangle has 4 ends, and these 4 crossings are the ones immediately outside the tangle
        a2idx=testKnot.index(seg1[0])-1
        b2idx=testKnot.index(seg1[-1])+1-len(testKnot)
        c2idx=testKnot.index(seg2[0])-1
        d2idx=testKnot.index(seg2[-1])+1-len(testKnot)
        a2=testKnot[a2idx]
        b2=testKnot[b2idx]
        c2=testKnot[c2idx]
        d2=testKnot[d2idx]
        a2S=signs[a2idx]
        b2S=signs[b2idx]
        c2S=signs[c2idx]
        d2S=signs[d2idx]

        #Look at the 4 outer ends and see which ones compose the same crossing
        AB=abs(a2)==abs(b2)
        AC=abs(a2)==abs(c2)
        AD=abs(a2)==abs(d2)
        BC=abs(b2)==abs(c2)
        BD=abs(b2)==abs(d2)
        CD=abs(c2)==abs(d2)
        
        #See how many of these are true
        truths=0
        for item in (AB,AC,AD,BC,BD,CD):
            if item:
                truths=truths+1
        
        #if none of them or too many of them are true, this won't work, so we move on        
        if truths==0 or truths>=3:
            break
        
        
        #Create virtual lengths for the tangle parts
        #These count the number of actual interactions between the two parts
        #Which determines what type of tangle we're dealing with
        seglen1=len(seg1)
        seglen2=len(seg2)
        
        
        #If a crossing is completed within the same segment, the virtual length can be decreased by 1
        for item in seg1:
            if -item in seg1:
                seglen1=seglen1-0.5
                
        for item in seg2:
            if -item in seg2:
                seglen2=seglen2-0.5
        
        
        #The first type of tangle is when the number of interactions between the parts is even
        #The seglengths divided by 2 gives the number of crossings, so we divide by 2 again
        #to determine the parity of the number of crossings
        #thus the %4
        if (seglen1+seglen2)%4==0:
            #Find the first crossing in seg1 where the crossing is not self-completing,
            #but is rather an interaction between the two segments
            for x in range(len(seg1)):
                if -seg1[x] not in seg1 and -seg1[x] in seg2:
                    seg1start=seg1[x]
                    break
            #Same process for the last crossing
            for y in range(len(seg1)-1,0,-1):
                if -seg1[y] not in seg1 and seg1[y]!=seg1start and -seg1[y] in seg2:
                    seg1end=seg1[y]
                    break
            
            #There are sub-cases within the even number of crossings case
            #dependent on the orientation of each segment in relation to each other
            if seg2.index(-seg1start)<seg2.index(-seg1end):
                bottom="right"
            else:
                bottom="left"
                
            #And now the precise cases
            if a2==-b2:
                testKnot.remove(a2)
                testKnot.remove(b2)
                del signs[max(a2idx,b2idx)]
                del signs[min(a2idx,b2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]
                    
                
                if bottom=="right":
                    testKnot.insert(seg2StartIdx,a2)
                    testKnot.insert(seg2EndIdx+1,b2)
                    signs.insert(seg2StartIdx,a2S)
                    signs.insert(seg2EndIdx+1,b2S)
                    break
                    
                elif bottom=="left":
                    testKnot.insert(seg2StartIdx,b2)
                    testKnot.insert(seg2EndIdx+1,a2)
                    signs.insert(seg2StartIdx,b2S)
                    signs.insert(seg2EndIdx+1,a2S)
                    break

            elif a2==-c2 and bottom=="right":
                
                testKnot.remove(a2)
                testKnot.remove(c2)
                del signs[max(a2idx,c2idx)]
                del signs[min(a2idx,c2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i] 
      
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1EndIdx+1,a2)
                testKnot.insert(seg2EndIdx+1,c2)
                signs.insert(seg1EndIdx+1,a2S)
                signs.insert(seg2EndIdx+1,c2S)
                break
                
            elif b2==-d2 and bottom=="right":
                
                testKnot.remove(b2)
                testKnot.remove(d2)
                del signs[max(b2idx,d2idx)]
                del signs[min(b2idx,d2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]
    
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1StartIdx,b2)
                testKnot.insert(seg2StartIdx,d2)
                signs.insert(seg1StartIdx,b2S)
                signs.insert(seg2StartIdx,d2S)
                break
                
            elif a2==-d2 and bottom=="left":
                
                testKnot.remove(a2)
                testKnot.remove(d2)
                del signs[max(a2idx,d2idx)]
                del signs[min(a2idx,d2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]
    
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1EndIdx+1,a2)
                testKnot.insert(seg2StartIdx,d2)
                signs.insert(seg1EndIdx+1,a2S)
                signs.insert(seg2StartIdx,d2S)
                break
                
            elif b2==-c2 and bottom=="left":
                
                testKnot.remove(b2)
                testKnot.remove(c2)
                del signs[max(b2idx,c2idx)]
                del signs[min(b2idx,c2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]

                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1StartIdx,b2)
                testKnot.insert(seg2EndIdx+1,c2)
                signs.insert(seg1StartIdx,b2S)
                signs.insert(seg2EndIdx+1,c2S)
                break
                
        
        #Now the odd number of crossings case
        else:
            
            #A lot of mirroring occurs in these cases, so we have fewer precise cases to examine
            #because they are all covered by more general scenarios
            if a2==-c2:
                
                testKnot.remove(a2)
                testKnot.remove(c2)
                del signs[max(a2idx,c2idx)]
                del signs[min(a2idx,c2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]
                         
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1EndIdx+1,c2)
                testKnot.insert(seg2EndIdx+1,a2)
                signs.insert(seg1EndIdx+1,c2S)
                signs.insert(seg2EndIdx+1,a2S)
                break
                
            elif b2==-d2:
                
                testKnot.remove(b2)
                testKnot.remove(d2)
                del signs[max(b2idx,c2idx)]
                del signs[min(b2idx,c2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]
       
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1StartIdx,d2)
                testKnot.insert(seg2StartIdx,b2)
                signs.insert(seg1StartIdx,d2S)
                signs.insert(seg2StartIdx,b2S)
                break
                
            elif a2==-d2:

                testKnot.remove(a2)
                testKnot.remove(d2)
                del signs[max(a2idx,d2idx)]
                del signs[min(a2idx,d2idx)]
                
                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]       

                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1EndIdx+1,d2)
                testKnot.insert(seg2StartIdx,a2)
                signs.insert(seg1EndIdx+1,d2S)
                signs.insert(seg2StartIdx,a2S)
                break
                
            elif b2==-c2:
                
                testKnot.remove(b2)
                testKnot.remove(c2)
                del signs[max(b2idx,c2idx)]
                del signs[min(b2idx,c2idx)]

                seg1StartIdx=testKnot.index(seg1[0])-len(testKnot)
                seg1EndIdx=testKnot.index(seg1[-1])-len(testKnot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(testKnot)
                
                seg2StartIdx=testKnot.index(seg2[0])-len(testKnot)
                seg2EndIdx=testKnot.index(seg2[-1])-len(testKnot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(testKnot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    testKnot[i]=-testKnot[i]       

                for i in range(seg2StartIdx,seg2EndIdx+1):
                    testKnot[i]=-testKnot[i]

                testKnot.insert(seg1StartIdx,c2)
                testKnot.insert(seg2EndIdx+1,b2)
                signs.insert(seg1StartIdx,c2S)
                signs.insert(seg2EndIdx+1,b2S)
                break

    return (testKnot,signs)



def transMove2(testKnot,signs,tangle):
    done=0
    #The setup for this is identical to translation move 1. Please refer to the comments on that function
    for j in [-1,0]:
        if done==1:
            break
        
        seg1=tangle[j]
        seg2=tangle[j+1]

        a2idx=testKnot.index(seg1[0])-1
        b2idx=testKnot.index(seg1[-1])+1-len(testKnot)
        c2idx=testKnot.index(seg2[0])-1
        d2idx=testKnot.index(seg2[-1])+1-len(testKnot)
        a2=testKnot[a2idx]
        b2=testKnot[b2idx]
        c2=testKnot[c2idx]
        d2=testKnot[d2idx]
        a2S=signs[a2idx]
        b2S=signs[b2idx]
        c2S=signs[c2idx]
        d2S=signs[d2idx]
        a1idx=testKnot.index(-a2)
        b1idx=testKnot.index(-b2)
        c1idx=testKnot.index(-c2)
        d1idx=testKnot.index(-d2)
        
        seglen1=len(seg1)
        seglen2=len(seg2)
        
        
        for item in seg1:
            if -item in seg1:
                seglen1=seglen1-0.5
                
        for item in seg2:
            if -item in seg2:
                seglen2=seglen2-0.5
        
        #Even number of crossings
        if (seglen1+seglen2)%4==0:
            for x in range(len(seg1)):
                if -seg1[x] not in seg1 and -seg1[x] in seg2:
                    seg1start=seg1[x]
                    break
            for y in range(len(seg1)-1,0,-1):
                if -seg1[y] not in seg1 and seg1[y]!=seg1start and -seg1[y] in seg2:
                    seg1end=seg1[y]
                    break
            
            
            if seg2.index(-seg1start)<seg2.index(-seg1end):
                bottom="right"
            else:
                bottom="left"       
            
            
            #The precise cases and how we look for them are where move 1 and move 2 differ
            if a2/abs(a2)==b2/abs(b2) and abs(a1idx-b1idx)==1:
                testKnot.remove(a2)
                testKnot.remove(b2)
                del signs[max(a2idx,b2idx)]
                del signs[min(a2idx,b2idx)]
                
                if bottom=="right":
                    idx=testKnot.index(seg2[0])
                    testKnot.insert(idx,a2)
                    signs.insert(idx,a2S)
                    
                    idx=testKnot.index(seg2[-1])+1-len(testKnot)
                    testKnot.insert(idx,b2)
                    signs.insert(idx,b2S)
                    
                    
                elif bottom=="left":
                    idx=testKnot.index(seg2[-1])+1-len(testKnot)
                    testKnot.insert(idx,a2)
                    signs.insert(idx,a2)
                    
                    idx=testKnot.index(seg2[0])
                    testKnot.insert(idx,b2)
                    signs.insert(idx,b2S)     
                                
                break           
            
            
            elif bottom=="right" and a2/abs(a2)==c2/abs(c2) and abs(a1idx-c1idx)==1:
                testKnot.remove(a2)
                testKnot.remove(c2)
                del signs[max(a2idx,c2idx)]
                del signs[min(a2idx,c2idx)]
                
                idx=testKnot.index(seg1[-1])+1-len(testKnot)
                testKnot.insert(idx,a2)
                signs.insert(idx,a2S)
                
                idx=testKnot.index(seg2[-1])+1-len(testKnot)
                testKnot.insert(idx,c2)
                signs.insert(idx,c2S)
                break
                
            elif bottom=="right" and b2/abs(b2)==d2/abs(d2) and abs(b1idx-d1idx)==1:
                testKnot.remove(b2)
                testKnot.remove(d2)
                del signs[max(b2idx,d2idx)]
                del signs[min(b2idx,d2idx)]
                
                idx=testKnot.index(seg1[0])
                testKnot.insert(idx,b2)
                signs.insert(idx,b2S)
                
                idx=testKnot.index(seg2[0])
                testKnot.insert(idx,d2)
                signs.insert(idx,d2S)
                break
                
            elif bottom=="left" and a2/abs(a2)==d2/abs(d2) and abs(a1idx-d1idx)==1:
                testKnot.remove(a2)
                testKnot.remove(d2)
                del signs[max(a2idx,d2idx)]
                del signs[min(a2idx,d2idx)]
                
                idx=testKnot.index(seg1[-1])+1-len(testKnot)
                testKnot.insert(idx,a2)
                signs.insert(idx,a2S)
                
                idx=testKnot.index(seg2[0])
                testKnot.insert(idx,d2)
                signs.insert(idx,d2S)
                break
            
            elif bottom=="left" and b2/abs(b2)==c2/abs(c2) and abs(b1idx-c1idx)==1:
                testKnot.remove(b2)
                testKnot.remove(c2)
                del signs[max(b2idx,c2idx)]
                del signs[min(b2idx,c2idx)]
                
                idx=testKnot.index(seg1[0])
                testKnot.insert(idx,b2)
                signs.insert(idx,b2S)
                
                idx=testKnot.index(seg2[-1])+1-len(testKnot)
                testKnot.insert(idx,c2)
                signs.insert(idx,c2S)
                break
        
        
        #Odd number of crossings
        else:    
            if a2/abs(a2)==c2/abs(c2) and abs(a1idx-c1idx)==1:
                testKnot.remove(a2)
                testKnot.remove(c2)
                del signs[max(a2idx,c2idx)]
                del signs[min(a2idx,c2idx)]
                
                idx=testKnot.index(seg2[-1])+1-len(testKnot)
                testKnot.insert(idx,a2)
                signs.insert(idx,a2S)
                
                idx=testKnot.index(seg1[-1])+1-len(testKnot)
                testKnot.insert(idx,c2)
                signs.insert(idx,c2S)
                break
                
            elif b2/abs(b2)==d2/abs(d2) and abs(b1idx-d1idx)==1:
                testKnot.remove(b2)
                testKnot.remove(d2)
                del signs[max(b2idx,d2idx)]
                del signs[min(b2idx,d2idx)]
                
                idx=testKnot.index(seg2[0])
                testKnot.insert(idx,b2)
                signs.insert(idx,b2S)
                
                idx=testKnot.index(seg1[0])
                testKnot.insert(idx,d2)
                signs.insert(idx,d2S)
                break
                
            elif a2/abs(a2)==d2/abs(d2) and abs(a1idx-d1idx)==1:
                testKnot.remove(a2)
                testKnot.remove(d2)
                del signs[max(a2idx,d2idx)]
                del signs[min(a2idx,d2idx)]
                
                idx=testKnot.index(seg2[0])
                testKnot.insert(idx,a2)
                signs.insert(idx,a2S)
                
                idx=testKnot.index(seg1[-1])+1-len(testKnot)
                testKnot.insert(idx,d2)
                signs.insert(idx,d2S)
                break
            
            elif b2/abs(b2)==c2/abs(c2) and abs(b1idx-c1idx)==1:
                testKnot.remove(b2)
                testKnot.remove(c2)
                del signs[max(b2idx,c2idx)]
                del signs[min(b2idx,c2idx)]
                
                idx=testKnot.index(seg2[-1])+1-len(testKnot)
                testKnot.insert(idx,b2)
                signs.insert(idx,b2S)
                
                idx=testKnot.index(seg1[0])
                testKnot.insert(idx,c2)
                signs.insert(idx,c2S)
                break
    
    return (testKnot,signs)

#Gauss Code Standardization for large list

#File=open("C:\Users\Brian\Google Drive\Knot Theory Independent Work\Gauss Codes.txt","r")
##File2=open("C:\Users\Brian\Google Drive\Knot Theory Independent Work\Standardized Codes.txt","w")
#
#
#for line in File:
#    knot=eval(line)
#    signs=[]
#    name(knot,signs)
#    raw_input()
#    #File2.write(str(knot)+'\n')
#    if knot==[]:
#        File.close()
#        #File2.close()
#        break


