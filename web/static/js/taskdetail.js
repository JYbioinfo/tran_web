/**
 * Created by guhongjie on 2015/12/14.
 */
function save()
{
    name_zh = document.getElementById("name_zh").value;
    text_zh = document.getElementById("text_zh").value;
    sys_no = document.getElementById("diseaseNo").value;
    var dic = {"disease_name_zn":name_zh,"text_zn":text_zh,"sys_no":sys_no}
    dic.toJSONString()

}
function submit()
{
    name_zh = document.getElementById("name_zh").value;
    text_zh = document.getElementById("text_zh").value;
}