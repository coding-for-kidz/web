const Range = ace.require("ace/range").Range;

$(document).ready(function () {
  //editor
  $(".editor").each(function (index) {
    const editor = ace.edit(this);
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/html");
    editor.session.setValue("<!DOCTYPE HTML>\n<html lang='en'>\n\t<head>\n\t</head>\n\t<body>\n\t\t<h1>Hello World</h1>\n\t</body>\n</html>"); // default value in editor
    $(this).data("aceObject", editor);
  });

});

function runit(editorElem) {
  $("#output").html(function () {
      const editor = $(editorElem).data("aceObject");
      return editor.session.getValue();
  });
}
