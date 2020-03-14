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
j=0
n=1000000001930000000057;
a= 92602129;
b=47915934;
c=-10798863015269;
M=500
AR(M)=j=-M;
while(j<M,j=j+1;X=( a*j^2+2*b*j+c);print(j,": ",X,": ", factor(X)))



n=87463;
B=50;
M=50;
a=29;
b=12;
c=-3011;
AR(M)=j=-M;
while(j<M,j=j+1;X=( a*j^2+2*b*j+c);print(j,": ",X,": ", factor(X)))
for(k=-50000,50000,n=10^20+k;aa=factor(n);if(aa[length(mattranspose(aa)),1]<B,print(n,": ",aa),))


aa=factor(X);
if(aa[length(mattranspose(aa)),1]<B

print("stampa alcuni numeri dell'array di sieving")
AR(N,M)=j=0;
while(j<M,j=j+1;X=((trunc(N^(1/2))+j)^2-N);print(j,": ",X,".", factor(X)))
print("stampa solo il fattore massimo")
AR(N,M)=j=0;
while(j<M,j=j+1;X=((truncate(N^(1/2))+j)^2-N);ff=factor(X);ll=length(mattranspose(ff));r=ff[ll,1];print(j, ":" , "fattore massimo =  ",r));

AR(N,M)=j=-M;
while(j<M,j=j+1;X=((truncate(N^(1/2))+j)^2-N);ff=factor(X);ll=length(mattranspose(ff));r=ff[ll,1];print(j, ":", "fattore massimo =  ",r));
print("stampa solo il fattore massimo dei numeri B-smooth")

AR(N,M,B)=j=-M;
while(j<M,j=j+1;X=((truncate(N^(1/2))+j)^2-N);ff=factor(X,B);ll=length(mattranspose(ff));r=ff[ll,1];if(r<B,print(j, ":",X,":", "fattore massimo =  ",r)));

print("usando solo fattori minori di B, scrive numeri B-smooth intorno a sqrtN in un array di ampiezza M")
N=n;
AR(N,M,B)=j=-M; while(j<M,j=j+1;X=((truncate(N^(1/2))+j)^2-N);ff=factor(X,B);ll=length(mattranspose(ff));r=ff[ll,1];if(r<B,print(j, " :",X,":", ff,"    :", "fattore massimo =  ",r)));

if(r<B,print(j,":", "fattore massimo =  ",r)));

n = 6656800545806786369367511893893
a 120564458468459207527134264992
b 3377268347268212146162102380774
