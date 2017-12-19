
	$("li").click(function(){
		$("li").not(this).each(function(){
		 $(this).first().addClass("active").nextAll().removeClass("active");
	     });
	     $(this).addClass("active");
	})
	$("#newDeckAdd").hide();
// 	$("#newDeck").click(function(){
// 		$("#newDeck").html("Add to Existing Deck");
// 		$("#newDeckAdd").toggle(1000);
// 		$("#addExisting").toggle(1000);
// 		console.log('toggle');
// 	});

  $("div .item").load().first().addClass("active");
  console.log("this happened");
