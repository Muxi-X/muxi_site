 // datepicker
 // By StephenLiu

$(document).ready(function(){
    //公开的的对象
    var calendar = {
        //对应input输入组件的id
        targetInputBoxId: null,
        //下拉框最大年份
        maxYear: 2050,
        //下拉框最小年份
        minYear: 1900,
        //使用控件的接口
        init: null,
        //显示控件事件
        showEvent: null,
        //关闭控件事件
        closeEvent: null,
        //前一个月事件
        preMonthEvent: null,
        //下一个月事件
        nextMonthEvent: null,
        //下拉框改变时触发的事件
        selectChangeEvent: null,
        //点击日历某一天的事件
        selectDayEvent: null,
        //关闭事件
        outBoxEvent: null
    };
    //封装控件中使用的元素的id
    var calendarBox = {
        //最外层id
        boxId : "calendar_box",
        //年选择下拉id
        selYearId: "calendar_sel_Year",
        //月选择下拉id
        selMonthId: "calendar_sel_moth",
        //选择前一个月的id
        preMonthId: "calendar_preMonthId",
        //选择下一个月的id
        nextMonthId: "calendar_nextMonthId",
        //显示日期列表元素的id
        dayListBoxId: "calendar_dayList" ,
        //关闭按钮id
        btnDone: "calendar_btnDone"
    };

    //初始化html
    var initHtml = function(){
        var box = document.getElementById(calendarBox.boxId);
        if(!box){
            //加载样式
            var tempElement = document.createElement("div");
            var parent = document.getElementsByTagName("head")[0] || document.documentElement;
            var style = "x" + calendarStyle;
            tempElement.innerHTML = style;
            parent.appendChild(tempElement.lastChild);
            //加载html
            tempElement.innerHTML = calendarHtml;
            document.body.appendChild(tempElement.firstChild);
        }
    };
    //初始化年选择
    var initSelYear = function(){
        var yearSel = document.getElementById(calendarBox.selYearId);
        //若该值为赋值或不是数字时，设置一个默认值
        if(!calendar.minYear || typeof(+calendar.minYear) !== "number"){
            calendar.minYear = 1900;
        }
        if(!calendar.maxYear || typeof(+calendar.maxYear) !== "number"){
            calendar.maxYear = 2050;
        }
        yearSel.innerHTML = "";
        for (var i = calendar.maxYear ; i >= calendar.minYear ; i--) {
            var optionElement = document.createElement("option");
            optionElement.value = i;
            optionElement.innerHTML = i;
            yearSel.appendChild(optionElement);
        }
    };
    //初始化月选择
    var initSelMonth = function () {
        var monthSel = document.getElementById(calendarBox.selMonthId);
        for (var i = 1; i <= 12; i++) {
            var optionElement = document.createElement("option");
            optionElement.value = i;
            optionElement.innerHTML = i + "月";
            monthSel.appendChild(optionElement);
        }
    };
    //绑定事件
    var initEvent = function(){
        addEvent("focus", document.getElementById(calendar.targetInputBoxId), calendar.showEvent);
        addEvent("click", document.getElementById(calendarBox.btnDone), calendar.closeEvent);
        addEvent("click", document.getElementById(calendarBox.preMonthId), calendar.preMonthEvent);
        addEvent("click", document.getElementById(calendarBox.nextMonthId), calendar.nextMonthEvent);
        addEvent("click", document, calendar.outBoxEvent);
        addEvent("change", document.getElementById(calendarBox.selYearId), calendar.selectChangeEvent);
        addEvent("change", document.getElementById(calendarBox.selMonthId), calendar.selectChangeEvent);
    };
    //显示日历
    var displayDate = function(newDate){
        if(!newDate){
            return;
        }
        var year = newDate.getFullYear();
        var month = newDate.getMonth() + 1;
        var today = new Date();
        //获取第一天时星期几
        var firstWeekDay = new Date(year,month - 1,1).getDay();
        //获取当前月份天数
        var dates = new Date(year,month,0).getDate();
        var yearSel = document.getElementById(calendarBox.selYearId);
        var mothsel = document.getElementById(calendarBox.selMonthId);
        var dateBox = document.getElementById(calendarBox.dayListBoxId);

        yearSel.value = year;
        mothsel.value = month;

        dateBox.innerHTML = "";

        //填补前面的空白
        for (var k = 0; k < firstWeekDay; k++) {
            var liElement = document.createElement("li");
            dateBox.appendChild(liElement);
        }
        //填充日期
        for (var i = 1; i <= dates; i++) {
            var liElement = document.createElement("li");
            var aElement = document.createElement("a");
            aElement.href = "javascript:void(0);";
            addEvent("click", aElement, calendar.selectDayEvent);
            if (i === today.getDate() && today.getFullYear() === year && today.getMonth() + 1 === month) {
                aElement.className = "selected";
            }
            aElement.innerHTML = i;
            liElement.appendChild(aElement);
            dateBox.appendChild(liElement);
        }

    };

    //初始化函数,定义接口
    calendar.init = function(targetInput){
        if(targetInput){
            calendar.targetInputBoxId = targetInput;
        }
        initHtml();
        initSelYear();
        initSelMonth();
        initEvent();
        displayDate(new Date());
    };
    //选取某天触发的事件
    calendar.selectDayEvent = function(event){
        var evt = window.event || event;
        var target = evt.srcElement || evt.target;
        var year = document.getElementById(calendarBox.selYearId).value;
        var moth = document.getElementById(calendarBox.selMonthId).value;
        var day = target.innerHTML;
        var date = year + "-" + fix(moth) + "-" + fix(day);
        var inputBox = document.getElementById(calendar.targetInputBoxId);
        if(calendar.targetInputBoxId){
            inputBox.value = date;
        }
        calendar.closeEvent();

    };
    //下拉表触发事件
    calendar.selectChangeEvent = function(){
        var year = +document.getElementById(calendarBox.selYearId).value;
        var moth = +document.getElementById(calendarBox.selMonthId).value - 1;
        displayDate(new Date(year,moth,1));
    };
    //上一个月
    calendar.preMonthEvent = function () {
        var year = +document.getElementById(calendarBox.selYearId).value;
        //注意这里是减2，因为new Date里面的month比实际小1，减去1是当前选择的月份，减去2后new出来才是前一个月
        var moth = +document.getElementById(calendarBox.selMonthId).value - 2;
        displayDate(new Date(year, moth, 1));
    };
    //下一个月
    calendar.nextMonthEvent = function () {
        var year = +document.getElementById(calendarBox.selYearId).value;
        //注意这里不用加减，因为new Date里面的month比实际小1，所以本身指的就是下一个月
        var moth = +document.getElementById(calendarBox.selMonthId).value;
        displayDate(new Date(year, moth, 1));
    };
    //showEvent
    calendar.showEvent = function(event){
        var box = document.getElementById(calendarBox.boxId);
        var evt = window.event || event;
        var inputBox = evt.srcElement || evt.target;
        calendar.targetInputBoxId = inputBox.id;

        //将日历组件放在input下方
        box.style.left = getOffsetLeft(inputBox,0) + "px";
        box.style.top = (getOffsetTop(inputBox,0) + inputBox.offsetHeight) + "px";
        box.style.display = "block";

        inputBox.blur();
    };
    //closeEvent
    calendar.closeEvent = function(){
        var box = document.getElementById(calendarBox.boxId);
        if(box.style.display === "block"){
            box.style.display = "none";
        }
    };
    //outBoxEvent,点击组件外面关闭组件
    calendar.outBoxEvent = function(event){
        var evt = window.event || event;
        var target = evt.srcElement || evt.target;
        while (target.tagName.toLowerCase() != "body" && target.tagName.toLowerCase() != "html") {
            if (target.id === calendarBox.boxId || target.id === calendar.targetInputBoxId) {
                break;
            }
            target = target.parentNode;
        }
        if (!target.id || (target.id != calendarBox.boxId && target.id != calendar.targetInputBoxId)) {
            calendar.closeEvent();
        }
    };
    //定义添加事件的方法
    var addEvent = function(type,elem,fn){
        if(window.addEventListener){
            elem.addEventListener(type,fn);
        }
        else{
            elem.attachEvent("on" + type,fn);
        }
    };

    //获取到顶部的距离
    var getOffsetTop = function(obj,top){
        top = obj.offsetTop;
        if(obj.offsetParent != null ){
            top += getOffsetTop(obj.offsetParent);
        }
        return top;
    };

    //获取到左边的距离
    var getOffsetLeft = function(obj,left){
        left = obj.offsetLeft;
        if(obj.offsetParent != null){
            left += getOffsetLeft(obj.offsetParent);
        }
        return left;
    };
    //格式化月份为两位数
    var fix = function(month){
        return ("" + month).length < 2 ? ("0" + month) : "" + month;
    };
    //样式
    var calendarStyle = "" +      
        '<style type="text/css">' +
        '   .calendar-box{ position:absolute; width:250px; padding:5px; border:1px solid #332a1c; font-size:12px; display:none;line-height:1;background:#fff843}' +
        '   .calendar-box .select-head{height:20px; line-height:20px; padding:5px; background:#332a1c;}' +
        '   .calendar-box .select-head a{ float:left; height:20px; width:20px; line-height:20px; background:#FFFFFF; color: #332a1c; text-decoration:none; text-align:center;}' +
        '   .calendar-box .select-head .select-month{ float:left;width:90px; height:20px; margin-left:5px; border:none;}' +
        '   .calendar-box .select-head .select-year{ float:left;width:90px; height:20px; margin-right:5px; border:none;margin-left:5px;}' +
        '   .calendar-box .day-box{ margin-top:8px;width:250px;}' +
        '   .calendar-box .day-box .th{ font-weight:bold; padding:5px 0; margin-bottom:5px; background:#332a1c; color:White; font-size:11px;}' +
        '   .calendar-box .day-box .th li{ display:inline-block; width:32px; text-decoration:none; text-align:center;}' +
        '   .calendar-box .day-box .list-box{clear:both; float:left;padding-left:3px;}' +
        '   .calendar-box .day-box .list-box li{display:inline-block; width:35px; margin:0 2x 4px 0;}' +
        '   .calendar-box .day-box .list-box a{width:100%; height:20px; line-height:20px; display:inline-block; text-decoration:none; background:#332a1c; color:White; text-align:center;}' +
        '   .calendar-box .day-box .list-box a:hover{ background:#eee;color:#332a1c;outline:1px solid #332a1c;}' +
        '   .calendar-box .day-box .list-box .selected{ background:#eee; color:#332a1c;outline:1px solid #332a1c;}' +
        '   .calendar-box ul,.calendar-box li{ display:inline-block; list-style:none; padding:0; margin:0;}' +
        '   .calendar-box .btn-box{clear:both; padding:5px 4px; font-size:11px;}' +
        '   .calendar-box .btn-box .donebtn{ float:right;}' +
        '   .calendar-box .btn-box a{ float:left; padding:5px; text-decoration:none; background:#332a1c; color:White;}' +
        '   .calendar-box .btn-box a:hover{ background:#eee; color:#332a1c;}' +
        '</style>';
    //html
    var calendarHtml = "" +
    '<div id="calendar_box" class="calendar-box">' +
    '    <div class="select-head">' +
    '        <a id="calendar_preMonthId" href="javascript:;" ><<</a>' +
    '        <select id="calendar_sel_moth" class="select-month">' +
    '        </select>' +
    '        <select id="calendar_sel_Year" class="select-year">' +
    '        </select>' +
    '        <a id="calendar_nextMonthId" href="javascript:;" >>></a>' +
    '    </div>' +
    '    <div class="day-box">' +
    '        <ul class="th">' +
    '            <li>' +
    '                <span>日</span>' +
    '            </li>' +
    '            <li>' +
    '                <span>一</span>' +
    '            </li>' +
    '            <li>' +
    '                <span>二</span>' +
    '            </li>' +
    '            <li>' +
    '                <span>三</span>' +
    '            </li>' +
    '            <li>' +
    '                <span>四</span>' +
    '            </li>' +
    '            <li>' +
    '                <span>五</span>' +
    '            </li>' +
    '            <li>' +
    '                <span>六</span>' +
    '            </li>' +
    '        </ul>' +
    '        <ul id="calendar_dayList" class="list-box">' +
    '        </ul>' +
    '    </div>' +
    '    <div class="btn-box">' +
    '        <a id="calendar_btnDone" class="donebtn" href="javascript:;">关闭</a>' +
    '    </div>' +
    '</div>';

    //interface
    window.$c = window.$c || {};
    window.$c.calendar = calendar;


});