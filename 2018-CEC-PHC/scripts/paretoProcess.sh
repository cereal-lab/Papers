#!/bin/bash
ecj_data_processing() {
 for i in ./*.ParetoFrequency.txt
    do
     cut -f1 -d ' ' $i > ./$i.ParentDominates
     cut -f2 -d ' ' $i > ./$i.NonComparable
     cut -f3 -d ' ' $i > ./$i.ChildDominates  
     cut -f4 -d ' ' $i > ./$i.Equal
     cut -f5 -d ' ' $i > ./$i.Equivalent
     #-f says which field you want to extract, -d says what is the field delimeter that is used in the input file 
    done

  paste *.ParentDominates > ParentDominates.all
  paste *.NonComparable > NonComparable.all
  paste *.ChildDominates > ChildDominates.all
  paste *.Equal > Equal.all
  paste *.Equivalent > Equivalent.all

 
  rm *.ParentDominates
  rm *.NonComparable
  rm *.ChildDominates
  rm *.Equal
  rm *.Equivalent
}
ecj_data_processing
