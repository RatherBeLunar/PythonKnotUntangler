import Name
            


def move1(knot,signs):
    for i in range(-len(knot),0):
        a=knot[i]
        b=knot[i+1]
        
        #if the crossings are adjacent, thus forming a loop...
        if a==-b:
            #delete the twist
            del signs[knot.index(a)]
            knot.remove(a)
            del signs[knot.index(b)]
            knot.remove(b)
        
            if auto==0:
                print "move 1 worked"
                print "Knot: ", knot
                raw_input()
            return (knot,signs)
            break


def move1Works(knot):
    for i in range(-len(knot),0):
        if knot[i]==-knot[i+1]:
            return True
            break
    else:
        return False


def move2(knot,signs):
    for i in range(-len(knot),0):
        #search adjacent crossings
        a=knot[i]
        b=knot[i+1]
        
        if (a/abs(a))!=(b/abs(b)):
            continue
            
        if abs(knot.index(-a)-knot.index(-b))==1:
            
            del signs[knot.index(a)]
            knot.remove(a)
            del signs[knot.index(-a)]
            knot.remove(-a)
            del signs[knot.index(b)]
            knot.remove(b)
            del signs[knot.index(-b)]
            knot.remove(-b)
            
            if auto==0:
                print "move 2 worked"
                print "Knot: ", knot
                raw_input()
            
            return (knot,signs)
            break  


def move2Works(knot):
    for i in range(-len(knot),0):
        a=knot[i]
        b=knot[i+1]        
        if (a/abs(a))==(b/abs(b)) and abs(knot.index(-a)-knot.index(-b))==1:
            return True
            break
    else:
        return False
              

#Finds all the tangles of a given size in the knot
def findTangles(knot,size):
    if size==0:
        return
    else:
        #tangles holds a list of all the tangles found
        tangles=[]
        for a in range(-len(knot),0):
            idxA=a
            
            #segA finds the first half segment of a tangle
            #There are two segments to a tangle, they complete each others' crossings
            segA=[knot[idxA]]
            
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
                if idxA==len(knot)-1:
                    break
                
                #If a crossing completes itself in segA, then segA has more than the given size of crossings
                #So segB doesn't need to contain as many
                #With this, we do not increase the virtual length of segA
                if -knot[idxA] in segA:
                    sizeB=sizeB-1
                    segA.append(knot[idxA])
                
                #If the crossing is unique, we simply add it, increase the virtual length of segA
                #and continue
                else:
                    segA.append(knot[idxA])
                    lensegA=lensegA+1
            
            
            #Now we have a completed segA, and we can create a segB that is "dependent" on segA
            for b in range(-len(knot),0):
                idxB=b
                
                #Create an initial segB
                segB=[knot[idxB]]
                while len(segB)!=sizeB:
                    #Move to the next index in the knot
                    idxB=idxB+1
                    
                    #if we reach the end of the knot, stop
                    if idxB==len(knot)-1:
                        break
                    
                    #Here we can just add items to segB until we complete the size requirement
                    #We're about to test the validity of the segments anyway, so we can be simple here
                    segB.append(knot[idxB])
                
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
                        if (segB,segA) not in tangles and len(segA)<len(knot)/2 and len(segB)<len(knot)/2:
                            tangles.append((segA,segB))
                        break
    print tangles
    return tangles


def transMove1(knot,signs,tangle):
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
        a2idx=knot.index(seg1[0])-1
        b2idx=knot.index(seg1[-1])+1-len(knot)
        c2idx=knot.index(seg2[0])-1
        d2idx=knot.index(seg2[-1])+1-len(knot)
        a2=knot[a2idx]
        b2=knot[b2idx]
        c2=knot[c2idx]
        d2=knot[d2idx]

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
                knot.remove(a2)
                knot.remove(b2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]
                    
                
                if bottom=="right":
                    knot.insert(seg2StartIdx,a2)
                    knot.insert(seg2EndIdx+1,b2)
                    break
                    
                elif bottom=="left":
                    knot.insert(seg2StartIdx,b2)
                    knot.insert(seg2EndIdx+1,a2)
                    break

            elif a2==-c2 and bottom=="right":
                
                knot.remove(a2)
                knot.remove(c2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i] 
      
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1EndIdx+1,a2)
                knot.insert(seg2EndIdx+1,c2)
                break
                
            elif b2==-d2 and bottom=="right":
                
                knot.remove(a2)
                knot.remove(d2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]
    
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1StartIdx,b2)
                knot.insert(seg2StartIdx,d2)
                break
                
            elif a2==-d2 and bottom=="left":
                
                knot.remove(a2)
                knot.remove(d2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]
    
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1EndIdx+1,a2)
                knot.insert(seg2StartIdx,d2)
                break
                
            elif b2==-c2 and bottom=="left":
                
                knot.remove(b2)
                knot.remove(c2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]

                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1StartIdx,b2)
                knot.insert(seg2EndIdx+1,c2)
                break
                
        
        #Now the odd number of crossings case
        else:
            
            #A lot of mirroring occurs in these cases, so we have fewer precise cases to examine
            #because they are all covered by more general scenarios
            if a2==-c2:
                
                knot.remove(a2)
                knot.remove(c2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]
                         
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1EndIdx+1,c2)
                knot.insert(seg2EndIdx+1,a2)
                break
                
            elif b2==-d2:
                
                knot.remove(a2)
                knot.remove(c2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]
       
                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1StartIdx,d2)
                knot.insert(seg2StartIdx,b2)
                break
                
            elif a2==-d2:

                knot.remove(a2)
                knot.remove(d2)
                
                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]       

                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1EndIdx+1,d2)
                knot.insert(seg2StartIdx,a2)
                break
                
            elif b2==-c2:
                
                knot.remove(b2)
                knot.remove(c2)

                seg1StartIdx=knot.index(seg1[0])-len(knot)
                seg1EndIdx=knot.index(seg1[-1])-len(knot)
                if seg1EndIdx<seg1StartIdx:
                    seg1EndIdx=seg1EndIdx+len(knot)
                
                seg2StartIdx=knot.index(seg2[0])-len(knot)
                seg2EndIdx=knot.index(seg2[-1])-len(knot)
                if seg2EndIdx<seg2StartIdx:
                    seg2EndIdx=seg2EndIdx+len(knot)
                
                for i in range(seg1StartIdx,seg1EndIdx+1):
                    knot[i]=-knot[i]       

                for i in range(seg2StartIdx,seg2EndIdx+1):
                    knot[i]=-knot[i]

                knot.insert(seg1StartIdx,c2)
                knot.insert(seg2EndIdx+1,b2)
                break

    return knot



    
    
def transMove2(knot,signs,tangle):
    done=0
    
    #The setup for this is identical to translation move 1. Please refer to the comments on that function
    for j in [-1,0]:
        if done==1:
            break
        
        seg1=tangle[j]
        seg2=tangle[j+1]

        a2idx=knot.index(seg1[0])-1
        b2idx=knot.index(seg1[-1])+1-len(knot)
        c2idx=knot.index(seg2[0])-1
        d2idx=knot.index(seg2[-1])+1-len(knot)
        a2=knot[a2idx]
        b2=knot[b2idx]
        c2=knot[c2idx]
        d2=knot[d2idx]
        a1idx=knot.index(-a2)
        b1idx=knot.index(-b2)
        c1idx=knot.index(-c2)
        d1idx=knot.index(-d2)
        
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
                print tangle
                knot.remove(a2)
                knot.remove(b2)
                if bottom=="right":
                    knot.insert(knot.index(seg2[0]),a2)
                    knot.insert(knot.index(seg2[-1])+1-len(knot),b2)
                    
                elif bottom=="left":
                    knot.insert(knot.index(seg2[-1])+1-len(knot),a2)
                    knot.insert(knot.index(seg2[0]),b2)        
                
                beforeA=knot[knot.index(seg1[0])-1]
                afterB=knot[knot.index(seg1[-1])+1-len(knot)]
                
                if not move2Works(knot) and not move1Works(knot) and beforeA/abs(beforeA)==afterB/abs(afterB) and abs(knot.index(-beforeA)-knot.index(-afterB))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                    
                break           
            
            
            elif bottom=="right" and a2/abs(a2)==c2/abs(c2) and abs(a1idx-c1idx)==1:
                print tangle
                knot.remove(a2)
                knot.remove(c2)
                knot.insert(knot.index(seg1[-1])+1-len(knot),a2)
                knot.insert(knot.index(seg2[-1])+1-len(knot),c2) 
                
                beforeA=knot[knot.index(seg1[0])-1]
                beforeC=knot[knot.index(seg2[0])-1]
                
                if not move2Works(knot) and not move1Works(knot) and beforeA/abs(beforeA)==beforeC/abs(beforeC) and abs(knot.index(-beforeA)-knot.index(-beforeC))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                
                break
                
            elif bottom=="right" and b2/abs(b2)==d2/abs(d2) and abs(b1idx-d1idx)==1:
                print tangle
                knot.remove(b2)
                knot.remove(d2)
                knot.insert(knot.index(seg1[0]),b2)
                knot.insert(knot.index(seg2[0]),d2)
                
                afterB=knot[knot.index(seg1[-1])+1-len(knot)]
                afterD=knot[knot.index(seg2[-1])+1-len(knot)]
                
                if not move2Works(knot) and not move1Works(knot) and afterB/abs(afterB)==afterD/abs(afterD) and abs(knot.index(-afterB)-knot.index(-afterD))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                
                break
                
            elif bottom=="left" and a2/abs(a2)==d2/abs(d2) and abs(a1idx-d1idx)==1:
                print tangle
                knot.remove(a2)
                knot.remove(d2)
                knot.insert(knot.index(seg1[-1])+1-len(knot),a2)
                knot.insert(knot.index(seg2[0]),d2)
                
                beforeA=knot[knot.index(seg1[0])-1]
                afterD=knot[knot.index(seg2[-1])+1-len(knot)]
                
                if not move2Works(knot) and not move1Works(knot) and beforeA/abs(beforeA)==afterD/abs(afterD) and abs(knot.index(-beforeA)-knot.index(-afterD))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                
                break
            
            elif bottom=="left" and b2/abs(b2)==c2/abs(c2) and abs(b1idx-c1idx)==1:
                print tangle
                knot.remove(b2)
                knot.remove(c2)
                knot.insert(knot.index(seg1[0]),b2)
                knot.insert(knot.index(seg2[-1])+1-len(knot),c2)                    
                
                beforeC=knot[knot.index(seg2[0])-1]
                afterB=knot[knot.index(seg1[-1])+1-len(knot)]
                
                if not move2Works(knot) and not move1Works(knot) and afterB/abs(afterB)==beforeC/abs(beforeC) and abs(knot.index(-afterB)-knot.index(-beforeC))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                    
                break
        
        
        #Odd number of crossings
        else:    
            if a2/abs(a2)==c2/abs(c2) and abs(a1idx-c1idx)==1:
                print tangle
                knot.remove(a2)
                knot.remove(c2)
                knot.insert(knot.index(seg2[-1])+1-len(knot),a2)
                knot.insert(knot.index(seg1[-1])+1-len(knot),c2)
                
                beforeA=knot[knot.index(seg1[0])-1]
                beforeC=knot[knot.index(seg2[0])-1]
                
                if not move2Works(knot) and not move1Works(knot) and beforeA/abs(beforeA)==beforeC/abs(beforeC) and abs(knot.index(-beforeA)-knot.index(-beforeC))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                break
                
            elif b2/abs(b2)==d2/abs(d2) and abs(b1idx-d1idx)==1:
                print tangle
                knot.remove(b2)
                knot.remove(d2)
                knot.insert(knot.index(seg2[0]),b2)
                knot.insert(knot.index(seg1[0]),d2)

                afterB=knot[knot.index(seg1[-1])+1-len(knot)]
                afterD=knot[knot.index(seg2[-1])+1-len(knot)]
                
                if not move2Works(knot) and not move1Works(knot) and afterB/abs(afterB)==afterD/abs(afterD) and abs(knot.index(-afterB)-knot.index(-afterD))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                break
                
            elif a2/abs(a2)==d2/abs(d2) and abs(a1idx-d1idx)==1:
                print tangle
                knot.remove(a2)
                knot.remove(d2)
                knot.insert(knot.index(seg2[0]),a2)
                knot.insert(knot.index(seg1[-1])+1-len(knot),d2)
                
                beforeA=knot[knot.index(seg1[0])-1]
                afterD=knot[knot.index(seg2[-1])+1-len(knot)]                
                
                if not move2Works(knot) and not move1Works(knot) and beforeA/abs(beforeA)==afterD/abs(afterD) and abs(knot.index(-beforeA)-knot.index(-afterD))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                break
            
            elif b2/abs(b2)==c2/abs(c2) and abs(b1idx-c1idx)==1:
                print tangle
                knot.remove(b2)
                knot.remove(c2)
                knot.insert(knot.index(seg2[-1])+1-len(knot),b2)
                
                beforeC=knot[knot.index(seg2[0])-1]
                afterB=knot[knot.index(seg1[-1])+1-len(knot)]

                knot.insert(knot.index(seg1[0]),c2)
                if not move2Works(knot) and not move1Works(knot) and afterB/abs(afterB)==beforeC/abs(beforeC) and abs(knot.index(-afterB)-knot.index(-beforeC))==1:
                    print "running again with", tangle
                    knot=transMove2(knot[:],signs,tangle)
                break
    
    return knot   
        
    
            

    
            

#Runs 1 instance of attempting to untangle the knot
#by performing move1, move2, or move3 based on what should happen next
def step():
    global knot
    global signs
    global movenext
    if knot!=[]:
        #When determining which moves to perform first, we prioritize reduction Move 2's
        #Because they reduce more crossings at once, bringing down the number of steps required to untangle
        
        #test reduction moves
        if move2Works(knot):
            knot=(move2(knot[:],signs[:]))[:]
        elif move1Works(knot):
            knot=(move1(knot[:],signs[:]))[:]
        
        #If reduction moves don't work, examine translation moves
        else:
            
            #See if any translation move 2 results in a reduction move 2 becoming possible
            done=0
            for size in range(len(knot),0,-1):
                if done==1:
                    break
                tangles=(findTangles(knot[:],size))[:]
                for i in range(len(tangles)*2):
                    if move2Works(transMove2(knot[:],signs[:],tangles[i])):
                        knot=(transMove2(knot[:],signs[:],tangles[i]))[:]
                        if auto==0:
                            print "Translation Move 2 worked"
                            print "Knot: ",knot
                            raw_input()
                        done=1
                        break
            
            if done==0:
                #If no translation move 2 results in a reduction move 2, we try translation move 1
                #under the same criteria
                done=0
                for size in range(len(knot),1,-1):
                    if done==1:
                        break
                    tangles=(findTangles(knot[:],size))[:]
                    for i in range(len(tangles)*2):
                        if move2Works(transMove1(knot[:],signs[:],tangles[i])):
                            knot=(transMove1(knot[:],signs[:],tangles[i]))[:]
                            if auto==0:
                                print "Translation Move 1 worked"
                                print "Knot: ",knot
                                raw_input()
                            done=1
                            break
                if done==0:
                    #Repeat the examining process for translation moves followed by reduction move 1's
                    done=0
                    for size in range(len(knot),0,-1):
                        if done==1:
                            break
                        tangles=(findTangles(knot[:],size))[:]
                        for i in range(len(tangles)*2):
                            if move1Works(transMove2(knot[:],signs[:],tangles[i])):
                                knot=(transMove2(knot[:],signs[:],tangles[i]))[:]
                                if auto==0:
                                    print "Translation Move 2 worked"
                                    print "Knot: ",knot
                                    raw_input()
                                done=1
                                break
                    if done==0:
                        done=0
                        for size in range(len(knot),1,-1):
                            if done==1:
                                break
                            tangles=findTangles(knot,size)
                            for i in range(len(tangles)*2):
                                if move1Works(transMove1(knot[:],signs[:],tangles[i])):
                                    knot=(transMove1(knot[:],signs[:],tangles[i]))[:]
                                    if auto==0:
                                        print "Translation Move 1 worked"
                                        print "Knot: ",knot
                                        raw_input()
                                    done=1
                                    break
                        if done==0:
                            movenext="done"


#Central control
def unTangle():
    reset()
    global knot
    global signs
    Name.separate(knot,signs)
    if auto==0:
        print ""
        print "Gauss Code: ",knot
        print ""
        print "Handedness: ",signs
        print ""
        print "Untangling..."
        print ""
    while knot!=[] and movenext!="done":
        step()
    if knot==[]:
        print "This knot is the unknot"
        reset()
    elif len(knot)<6:
        print "This is not a valid knot"
        print "A knot must have at least 3 crossings"
        reset()
    else:
        Name.name(knot,signs)
        reset()
        
def reset():
    global movenext
    global signs
    global length
    movenext="move1"
    length=0
    signs=[]


#Set auto to 0 for a "debugging" mode,
#where information about what is happening to the knot is provided at every step
auto=0

#knot=eval(raw_input("Knot string:"))



#knot=[1,-2,3,-4,5,-1,-6,7,-8,9,2,-3,4,-5,-9,6,-7,8]
#knot=[1,-2,3,-1,4,-5,6,-7,5,-6,7,-4,2,-3]
#knot=[1,-2,3,4,-5,6,-7,-8,9,-1,2,-9,8,-3,-6,5,-4,7]
#knot=[1,-2,-3,4,-5,6,2,-7,8,-1,7,9,-4,5,-6,3,-9,-8]
#knot=[1,2,-3,-4,5,6,-7,-1,4,8,-9,-5,10,11,-12,-13,14,15,-16,-17,18,12,-15,-19,20,16,-11,-21,17,22,-23,-14,13,24,-22,-20,19,23,-24,-18,21,25,-6,-26,27,3,-2,-28,26,9,-8,-27,28,7,-25,-10]
#knot=[ -1, 2, 3, -4, -5, 6, -7, 1, 8, -3, 9, -10, 11, -9, 12, 5, -6, -13, 10, -11, -2, -8, 4, -12, 13, 7]
#knot=[1,-2,-3,4,5,-6,7,8,-9,-10,6,11,12,-13,2,-1,14,-7,10,-5,-11,-15,13,3,-8,9,-4,-12,15,-14]

#The Culprit
#knot=[1,-2,3,-4,5,6,7,-8,9,-3,4,-5,2,-1,-6,-9,10,-7,8,-10]

knot=[1,-2,3,-4,5,-6,7,-1,8,-9,10,-11,12,-13,-14,-5,15,-3,16,-17,9,18,19,14,20,-16,21,-8,22,-7,2,-21,17,-10,23,-24,25,-19,6,-15,4,-20,26,-12,27,-25,28,-23,11,-26,13,-27,24,-28,-18,-22]


















