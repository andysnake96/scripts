#!/usr/bin/bash
#!/usr/bin/bash
#!/bin/bash
copyrightAdd(){
for i in $(find .);
do
  if ! grep -q Copyright $i
  then
    cat copyright.txt $i >$i.new;
    mv $i.new $i
    rm $i.new
  fi
done
}
shebangAdd(){
python="#!/usr/bin/python3"
bash="#!/usr/bin/bash"
pari="usr/bin/env gp"
for FILE in $(find .);
do
  if [[ ${FILE##*.} == "py" ]];then
  	sed -i "1i$python" $FILE
  elif  [[ ${FILE##*.} == "sh" ]];then
  	sed -i "1i$bash" $FILE
  elif  [[ ${FILE##*.} == "sh" ]];then
  	sed -i "1i$pari" $FILE
  fi
done
}
copyrightAdd
shebangAdd
