#Copyright Andrea Di Iorio
#This file is part of scripts
#scripts is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#scripts is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with scripts.  If not, see <http://www.gnu.org/licenses/>.
#!/usr/bin/env gp



genSemiPrime(kernelSize10)={
	\\gen semiPrime grater then 10^kernelSize10
	\\with randomness added
	base=10^kernelSize10;
	print(type(base));
	rnd=random()%base;
	rnd2=random()%base;
	Q=nextprime(base+rnd);
	P=nextprime(base+rnd2);
	print("generated primes\t",P,"\t",Q);
	return(P*Q);
}
L(n)={
	exponent_rat=bestappr((log(n)*log(log(n)))^(0.5));
	L_n=exp(exponent_rat);
	return (ceil(L_n));
}


\\gen semiprime
PRIME_KERNEL_SIZE_10=16
\\n=genSemiPrime(PRIME_KERNEL_SIZE_10)

n=100000030925519250968982645360649
\\default tuning Crandal book
B=ceil(L(n)^(0.5))
M=ceil(L(n)^(0.5))-2000
print("L(n) tuning...> B: ",B,"M: ",M)
\\B=11000
\\M=15000
FactorBaseGen(start,lenght,n)={
	\\gen factor base of all prime in range [start,end]
	\\searching for primes that make n a quadratic residue mod p
	print("gen factor base in range ",start,"--",end);
	
	factorbase=List();
	l=0;
	forprime(p=start,,
		if(kronecker(n,p)==1,listput(factorbase,p);l+=1);
		if(l==lenght,break();));
	return(factorbase);
}

genB(a)={
	\\\\\\\\\\\\ GEN B --> contini
	b=0;
	a_factors=mattranspose(factor(a));
	print("a:  ",a_factors);
	for(l=1,l=length(a_factors),
		ql=a_factors[1,l];
		a_ql=a/ql;
		t_ql=sqrt(Mod(n,ql));
		w_ql=Mod(a/ql,ql)^-1;
		v=w_ql*t_ql;
		\\print("bgenDebug: \t gamma: ",v," ql: ",ql);
		if(lift(v)>(ql/2),
			v=ql-v;
			\\print("newGamma: ",v);
		);
		\\Bl=v*(a/ql);
		print("gamma: ",v," ql: ",ql," a/ql ",a_ql);
		b+=lift(v)*(a/ql);
	);
	return(b);
}
genPolCoeff_a_sequentially_centered(n,M,s,{start=0})={
	/*
		generating mongomery polinomial coefficient searching for 
			a-> start from threashold^(1/s) aggregating primes from left and right
			a must be square time a BSmooth num (Mongomery pol a*f(x)=(a*x^2+b)^2 )
	
		TODO triggered BSmoothness check of pol values
	*/

	\\\\\\\\\		GEN  a 

	a=1;
	SIMPQS_a_THREASHOLD=truncate(((2*n)^(0.5))/M);	\\contini
	print("generating a coefficient Bsmooth Square up to",SIMPQS_a_THREASHOLD," with coeff a=q1*..*qs with s: ",s);
	if(start==0,start=truncate(SIMPQS_a_THREASHOLD^(1/s)));	
	start=max(start,2068);						\\avoid small primes for a gen
	print("START -> ",start);
	\\search for first prime
	p=nextprime(start);
	a*=p;
	while(kronecker(n,p)!=1,p=nextprime(p+1));
	print("start prime: ",p);
	\\compose a of primes in factorbase until reached suggested dimension
	SUB_FACTOR_BASE_RADIUS_ABS=300;
	FACTORBASE=FactorBaseGen(max(start-SUB_FACTOR_BASE_RADIUS_ABS,1),SUB_FACTOR_BASE_RADIUS_ABS,n);
	prime_indx_right=0;
	prime_indx_left=0;
	for(i=1,i=length(FACTORBASE),		\\center the factor base prime search seq in THREASHOLD^(1/s)
		if(p==FACTORBASE[i],
			print("first prime indx: ",i);
			prime_indx_left=i-1;	
			prime_indx_right=i+1;
			break();
		,print(FACTORBASE[i]););
	);
	print(length(FACTORBASE));
	print("factor base indexe l: ",prime_indx_left," right: ",prime_indx_right);
	i=1;
	\\TODO a GENERATION ALTERNATIVES:
	while(a<SIMPQS_a_THREASHOLD,			\\TODO EXCEED THREASHOLD SIZE
	\\while((a*p)<SIMPQS_a_THREASHOLD,			\\TODO NOT EXCEED THREASHOLD SIZE
		if(i%2==0,				\\alternativelly evaluate factor base prime on left and right of list center
			p=FACTORBASE[prime_indx_right];
			prime_indx_right+=1;
		,				\\else
			p=FACTORBASE[prime_indx_left];
			prime_indx_left-=1;
		);
		a*=p; 				\\TODO Crandal say a has to be Bsmooth^2
		i+=1;
	);
	print("a: ",a," factors#:",i, " vs threashold: ",SIMPQS_a_THREASHOLD," delta ",a-SIMPQS_a_THREASHOLD," ~digits#: ",log(a-SIMPQS_a_THREASHOLD)/log(10));

    b=genB(a);
	print("b: ",b);
	c=(b^2-n)/a;
	print("c: ",c);
	
	pol_vers_1=((a*j+b)^2-n)/a;
	pol_vers_2=a*j^2+2*b*j+c; 
	if(pol_vers_2==pol_vers_1,print("ok"),print("polinomials doesn't match"));

	return([a,b,c]);
}
logCumulative(B,factors)={
	\\simulate log sieving
	\\return sum of log(factor) in factors up to B
	\\HP factors equal to transposed factors list
	logCumulativeOut=0;
	for(x=2,x=length(factors),		\\x=2 -> skip +-1 --
		if(factors[1,x]<B,logCumulativeOut+=log(factors[1,x]));	\\cumulate log only if factor are B smooth 
	);
	return(logCumulativeOut);
}


LARGE_PRIME_UPPERBOUND=40*B;
checkFor1LargePrime(B,primes_)={
	\\return large prime inside (B,LARGE_PRIME_UPPERBOUND] if it exist alone :))))
	\\primes list expected to be transposed 
	\\0 otherwhise
	lastPrime=primes_[1,length(primes_)];		\\highest prime in primes_
	if(LARGE_PRIME_UPPERBOUND >= lastPrime && lastPrime > B,	
		\\last prime is ok for 1 large prime variation constraints
		\\check if it is the only one
		\\TODO SMARTER CHECK ON PRIMALITY RESIUDE ..?
		for(x=1,x=length(primes_)-1,			\\indexes to navigate the prime array from the last to first checking for other large primes_
			y=length(primes_)-x;			\\hold prime indexes from previus of the last prime  (checked above...)
			prime_=primes_[1,y];
			if(LARGE_PRIME_UPPERBOUND>= prime_ && prime_ > B,
				\\if(random()%1231==0,print("more than 1 large primes_, skipping...."));	\\TODO debug print
				return (0);
			);
		);	
	, return (0);	\\else unbounded large prime => skip it
	);
	\\if not exited until here means only 1! large prime has ben founded
	\\so setting it to large primes map
	return(lastPrime);
}


SieveConcurrentBSmoothnessPolLargePrimeList(a,b,c,M,N,{start=0})={
	/* printing BSmooth values for Mongomery polinamial with coefficient a,b,c
	   sieve pol value for BSmooths values in [-M,M]	
	   concurrent factorization applied by pari-gp concurrent :))))
	*/
	print("polinomio: a ",a,"b ",b,"c ",c," M ",M,"start ",start);
	foundedBsmoothValues=0;
	BSMOOTHlOGTHREASHOLD=log(M*sqrt(n));					\\mpqs contini log threashold post sieving
	NONB_SMOOTH_PRINT_RECURR=10000;
	
	largePrimeList=List(); 						\\largePrime-->source pol value factors
	mapFunctionVals=Map();
	print("START val: ",a*j^2 +2*b*j + c);
	parfor(j=ceil(0),j=ceil(10*M),
		\\mattranspose(factorint(a*j^2 +2*b*j + c));
		mattranspose(factorint((a*j+b)^2-N));
			,						\\END PARALLEL EXPR
		polValueFactors						\\PARRALLEL EXEC VAR
			,
		a_fx=((a*j+b)^2-N);
		\\a_fx=(a*j^2 +2*b*j + c);
		polValueFactorsNum=length(polValueFactors);
		maxFactor=polValueFactors[1,polValueFactorsNum];
		\\print(maxFactor);
		if(maxFactor<B,
			factorsLogCumul=logCumulative(B,polValueFactors);
			print1(j,"-->a* polValue --> ",a_fx,"--->BSmooth factors---> ",polValueFactors,"--> maxFactor -->",maxFactor,"--> log factors cumulativs -->",factorsLogCumul);
			foundedBsmoothValues+=1;
			if(factorsLogCumul>BSMOOTHlOGTHREASHOLD,print1(" < Bsmoothnes threashold ",BSMOOTHlOGTHREASHOLD));
			print("");				\\ \n
			if(mapisdefined(mapFunctionVals,a_fx),
				print("ALREADY DEFINED KEY= a*f(x)-->old value: ",mapget(mapFunctionVals,a_fx));
				next();
			);
			mapput(mapFunctionVals,a_fx,polValueFactors)
			
		, \\ELSE 		---extra short gp syntax ;) ---
			\\largePrime=checkFor1LargePrime(B,polValueFactors);
			\\if(largePrime!=0,
			\\	listput(largePrimeList,[largePrime,polValueFactors]);					\\append large prime and correlated pol factorization
			\\);
			\\TODO  log cumulative check for nn bsmooth 
			\\if(j%NONB_SMOOTH_PRINT_RECURR==0,lgCumul=logCumulative(B,polValueFactors);print("\n\n\nnon Bsmooth val: ",polValueFactors," logCumul ",lgCumul,"is < log Threash: ",lgCumul<BSMOOTHlOGTHREASHOLD));
		);
	);
	print("log factors threas:",BSMOOTHlOGTHREASHOLD);
	print("total BSmoothValues: ",foundedBsmoothValues);
	print("num primes p<B ",primepi(B));
	listsort(largePrimeList);
	print(largePrimeList);
}

SieveTrivialBSmoothnessPolLargePrimeList(a,b,c,M,{start=0})={
	/* printing BSmooth values for Mongomery polinamial with coefficient a,b,c
		from start (dflt to 0) to start+M
	*/
	print("polinomio: a,b,c,M,start");
	print(a);
	print(b);
	print(c);
	print(M);
	print(start);
	foundedBsmoothValues=0;
	BSMOOTHlOGTHREASHOLD=log(M*sqrt(n));					\\mpqs contini log threashold post sieving
	NONB_SMOOTH_PRINT_RECURR=10000;
	
	/*
	 hashmap to hold large primes identified when founding polinomio values with a non BSMOOTH factorization...
	 that one will be inserted in map only if are the only 1 large prime inside the pol.value factorization and are upper bounded with defined LARGE_PRIME_UPPERBOUND
	 map collision will be printed 
		-->TODO script matching list?
	*/
	largePrimeList=List(); 						\\largePrime-->source pol value factors
	for(j=-M,j=M,
		\\a_fx=lift(Mod((a*j^2 +2*b*j + c),n));			\\TODO ONLY f(x) val version
		a_fx=lift(Mod(a*(a*j^2 +2*b*j + c),n));
		polValueFactors=mattranspose(factorint(a_fx));
		polValueFactorsNum=length(polValueFactors);
		maxFactor=polValueFactors[1,polValueFactorsNum];
		\\print(maxFactor);
		if(maxFactor<B,
			factorsLogCumul=logCumulative(B,polValueFactors);
			print1(j,"-->a* polValue --> ",a_fx,"--->BSmooth factors---> ",polValueFactors,"--> maxFactor -->",maxFactor,"--> log factors cumulativs -->",factorsLogCumul);
			foundedBsmoothValues+=1;
			if(factorsLogCumul>BSMOOTHlOGTHREASHOLD,print1(" < Bsmoothnes threashold ",BSMOOTHlOGTHREASHOLD));
			print("");				\\ \n
			/*if(mapisdefined(mapFunctionVals,a_fx),
				print("ALREADY DEFINED KEY= a*f(x)-->old value: ",mapget(mapFunctionVals,a_fx));
				next()											\\continue to next iter
			);
			mapput(mapFunctionVals,a_fx,polValueFactors)
			*/
		, \\ELSE 		---extra short gp syntax ;) ---
			largePrime=checkFor1LargePrime(B,polValueFactors);
			if(largePrime!=0,
				listput(largePrimeList,[largePrime,polValueFactors]);					\\append large prime and correlated pol factorization
			);
			\\TODO  log cumulative check for nn bsmooth 
			\\if(j%NONB_SMOOTH_PRINT_RECURR==0,lgCumul=logCumulative(B,polValueFactors);print("\n\n\nnon Bsmooth val: ",polValueFactors," logCumul ",lgCumul,"is < log Threash: ",lgCumul<BSMOOTHlOGTHREASHOLD));
		);
	);
	print("log factors threas:",BSMOOTHlOGTHREASHOLD);
	print("total BSmoothValues: ",foundedBsmoothValues);
	print("num primes p<B ",primepi(B));
	listsort(largePrimeList);
	print(largePrimeList);
}

SieveTrivialBSmoothnessPol(a,b,c,M,{start=0})={
	/* printing BSmooth values for Mongomery polinamial with coefficient a,b,c
		from start (dflt to 0) to start+M
	*/
	print("polinomio: a,b,c,M,start");
	print(a);
	print(b);
	print(c);
	print(M);
	print(start);
	foundedBsmoothValues=0;
	BSMOOTHlOGTHREASHOLD=log(M*sqrt(n));					\\mpqs contini log threashold post sieving
	NONB_SMOOTH_PRINT_RECURR=10000;
	\\mapFunctionVals=Map();						\\TODO collision function val check
	for(j=-M,j=M,
		\\a_fx=lift(Mod((a*j^2 +2*b*j + c),n));			\\TODO ONLY f(x) val version
		a_fx=lift(Mod(a*(a*j^2 +2*b*j + c),n));
		polValueFactors=mattranspose(factorint(a_fx));
		polValueFactorsNum=length(polValueFactors);
		maxFactor=polValueFactors[1,polValueFactorsNum];
		\\print(maxFactor);
		if(maxFactor<B,
			factorsLogCumul=logCumulative(B,polValueFactors);
			print(j,"-->a* polValue --> ",a_fx,"--->BSmooth factors---> ",polValueFactors,"--> maxFactor -->",maxFactor,"--> log factors cumulativs -->",factorsLogCumul);
			foundedBsmoothValues+=1;
			if(factorsLogCumul<BSMOOTHlOGTHREASHOLD,print1(" < Bsmoothnes threashold ",BSMOOTHlOGTHREASHOLD));
			print("");				\\ \n
			/*if(mapisdefined(mapFunctionVals,a_fx),
				print("ALREADY DEFINED KEY= a*f(x)-->old value: ",mapget(mapFunctionVals,a_fx));
				next()											\\continue to next iter
			);
			mapput(mapFunctionVals,a_fx,polValueFactors)
			*/
		, \\else TODO  log cumulative check for nn bsmooth 
		if(j%NONB_SMOOTH_PRINT_RECURR==0,
			lgCumul=logCumulative(B,polValueFactors);
			print("\n\n\nnon Bsmooth val: ",polValueFactors," logCumul ",lgCumul,"is < log Threash: ",lgCumul<BSMOOTHlOGTHREASHOLD));
		);
	);
	print("log factors threas:",BSMOOTHlOGTHREASHOLD);
	print("total BSmoothValues: ",foundedBsmoothValues);
	print("num primes p<B ",primepi(B));
}

listRange(sourceList,rangeStart,rangeEnd)={
	\\return sub list of source list between rangeStart and rangeEnd
	outList=List();
	for(i=rangeStart,i=rangeEnd,listput(outList,sourceList[i]));
	return(outList);
}

\\f()=CheckBSmoothnessPol(a,b,c,M)
\\f()
stackUp({newSize=800000000})=default(parisize,newSize) \\deflt increase stack to ...
\\stackUp()

\\generate mongomery polinomio coefficients in an array TODO (INVERT COMMENT OF NEXT 2 LINE FOR COEFF GEN/READ)
polCoeff=genPolCoeff_a_sequentially_centered(n,M,4)
\\polCoeff=readvec("polynomialCoeff")

a=polCoeff[1]; b=polCoeff[2]; \\c=polCoeff[3];
c=ceil((b^2-n)/a);
print("\n\n\n\ngenerated Pol Coeff a: ",a," b: ",b," c: ",c)
print(" N: ",n," B: ",B," M: ",M)
printf("\n\n\n\n\n\n\n\n\n")

x(j)=(a*j+b)
X(j)=(a*j+b)^2
ff(j)={(a*j+b)^2-n}
y(j)={a*(a*j^2+2*b*j+c)}
modn(v)=Mod(v,n)
\\modnSquareCheck(x,y)={print(Mod(x^2,n),"\n",Mod(y^2,n));return(Mod(x^2,n)==Mod(y^2,n))}

modnSquareXCheck(x,y)={
	if(modn(x^2)!=modn(y),print(modn(x^2),"\t!=\t",modn(y));return());
	if(issquare(y)==0,
		factors=mattranspose(factor(y));
		print(factors);
		for(i=1,i=length(factors),if(factors[2,i]%2!=0,print("not square factor: ",factors[1,i]," ^ ",factors[2,i])));
		return();
	);
	try1=lift(modn(x)-modn(sqrtint(y)));try2=lift(modn(x)+modn(sqrtint(y)));
	print("trys x+-y:\t",try1,"\t",try2,"\twith X=\t",modn(x),";\tY=\t",modn(sqrtint(y)));
	print("\n",gcd(try1,n),"\t",gcd(try2,n),"\n");
}
print("x(j)^2==a*f(j) ",(X(q))==(y(q)))
print("x(j)^2 == a*f(x) mod n ",modn(X(q))==modn(y(q)))
print("a*f(j)==(a*j+b)^2 -n) ",ff(q)==y(q))		\\alternative forms of pol
\\REPORT COUPLING MOD N PROOF
j1=9669;
j2=96;
print("aj+b\t",v1=(x(j1)^2))
print("a*f(j)\t",v2=y(j1))
modn(x(j1)^2)==modn(y(j1))
print("ff mod n",modn(v1))
modn((x(j1)*x(j2)))^2==modn((y(j1)*y(j2)))

print("DAIIIII")
\\any pol. values in array [-M,M] with concurrent sieve --> as gp factorize
\\SieveConcurrentBSmoothnessPolLargePrimeList(a,b,c,ceil(M),n);
\\SieveTrivialBSmoothnessPolLargePrimeList(a,b,c,ceil(M),n);
m()=modnSquareXCheck(X,Y)

default(colors,"green")
