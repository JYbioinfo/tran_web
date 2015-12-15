/**
 * Created by guhongjie on 2015/12/14.
 */
function update(flag,sys_no)
{
    name_zh = document.getElementById("name_zh").value;
    text_zh = document.getElementById("text_zh").value;

    var turnForm = document.createElement("form");
    document.body.appendChild(turnForm);
    turnForm.method = 'post';
    turnForm.action = '/tasks/'+sys_no+'/update';

     var newElement = document.createElement("input");
     newElement.setAttribute("name","disease_name_zn");
     newElement.setAttribute("type","hidden");
     newElement.setAttribute("value",name_zh);
     turnForm.appendChild(newElement);

     var textElement = document.createElement("input");
     textElement.setAttribute("name","text_zn");
     textElement.setAttribute("type","hidden");
     textElement.setAttribute("value",text_zh);
     turnForm.appendChild(textElement);

     var flagElement = document.createElement("input");
     flagElement.setAttribute("name","flag");
     flagElement.setAttribute("type","hidden");
     flagElement.setAttribute("value",flag);
     turnForm.appendChild(flagElement);

     turnForm.submit();
}
