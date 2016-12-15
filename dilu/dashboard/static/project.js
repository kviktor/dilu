$(function() {
  var spinner_class = "fa fa-fw fa-spin fa-spinner";
  var timer = 0;

  function mySearch () { 
      var q = $("input").val();
      var v = $("select").val();
      $.ajax({
        method: "GET",
        url: "/search/",
        data: {'q': q, 'v': v},
        success: function(data) {
          $("#content").html(data.content);
          $("#num-results").show().find("strong").text(data.num);
          $("button i").prop("class", "fa fa-fw fa-search");
          if(data.q) document.title = "dilu - " + q;
        }
      });
  };

  function validateSearch() {
      var q = $("input").val();
      if(q && q.length < 3) {
        $(".alert").show();
      }
      else if(q) {
        $(".alert").hide();
        $("button i").prop("class", spinner_class);
        mySearch();
      }
  }
  $("body").on('keyup', "input", function(e) {
    if (timer) {
        clearTimeout(timer);
    }
    timer = setTimeout(validateSearch, 250); 
  });

  $("select").change(function() {
    validateSearch();
  });

  $("body").on("click", ".show-code", function(e) {
    var code = $(this).closest(".dj-object").find("pre");
    hljs.highlightBlock(code[0]);
    code.slideToggle();
    e.preventDefault();
  });
});
