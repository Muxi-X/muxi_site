(function(window, document) {
	'use strict';
	var submitBtn = document.querySelector(".send_submit_btn");
	var titleInput = document.querySelector(".send_title");
	var shareInput = document.querySelector("#flask-pagedown-share");
	var snackbarContainer = document.querySelector('#demo-snackbar-example');
	submitBtn.addEventListener("click", function(e) {
		if (titleInput.value === "") {
			e.preventDefault();
			showSnackbar("请输入分享标题");
			return;
		}
		if (shareInput.value === "") {
			e.preventDefault();
			showSnackbar("请输入分享内容");
			return;
		}
		if (!document.querySelector('input[name="tag"]:checked')) {
			e.preventDefault();
			showSnackbar("请选择分享分类");
			return;
		}
	});

  var showSnackbar = function(message) {
    var data = {
      message: message,
      timeout: 2000,
    };
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
  }

})(window, document);