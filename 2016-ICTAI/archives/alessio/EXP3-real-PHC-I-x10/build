#!/bin/bash
DIRHOME='/home/tux/tinkering/evoparsons-experiments/'

DIRECJ="$DIRHOME/ecj/ec/"
DIRORG="$DIRHOME/commons-math3-3.6.1-src/src/main/java/org/"
DIRGECCO16="$DIRHOME/gecco16/"
DIRTMP=".codebase"
DIREXP=`pwd`

rm *.jar *.stat 
rm -rf $DIRTMP  

mkdir $DIRTMP
cd $DIRTMP


cp -r $DIRGECCO16 ./ 
cp -r $DIRECJ ./
cp -r $DIRORG ./

mv ./gecco16 ./ec/ 

javac -cp . ./org/apache/commons/math3/random/*.java 
javac -cp . ./org/apache/commons/math3/exception/*.java 
javac -cp . ./org/apache/commons/math3/exception/util/*.java 
javac -cp . ./org/apache/commons/math3/special/*.java 
javac -cp . ./org/apache/commons/math3/util/*.java 
javac -cp . ./org/apache/commons/math3/distribution/*.java 

javac -cp . ./org/apache/commons/math3/analysis/solvers/*.java 

javac -cp . ./ec/gecco16/*.java


if [ $? != 0 ] 
then 
	echo "Take another look to the source..."
	exit
fi

 
jar cfm ${DIREXP}/ECJ.jar ./ec/gecco16/manifest.mf ./ec/*.class ./ec/*/*.class ./ec/*/*/*.class ./org/apache/commons/math3/*/*.class ./org/apache/commons/math3/*/*/*.class 

cd $DIREXP
# getting the ECJ config file in our testing folder 
cp ./$DIRTMP/ec/gecco16/hillclimber.params ./
cp ./$DIRTMP/ec/gecco16/pareto.params ./
cp ./$DIRTMP/ec/gecco16/evoparsons.params ./
cp ./$DIRTMP/ec/gecco16/paretoEvoparsons.params ./
cp ./$DIRTMP/ec/gecco16/qualitativePareto.params ./
cp ./$DIRTMP/ec/gecco16/qualitativeHillclimber.params ./



