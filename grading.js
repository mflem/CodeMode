function grading(){
    var points = 0;
    var radioVal = $("input[name='quiz']:checked").val();
    var textVal = $("input[name='quiz'][type='text']").val();
    var correctAnswer = $('p').attr('data-answer');
    console.log(radioVal);
    console.log(textVal);
    console.log(correctAnswer);
    if (radioVal == correctAnswer || textVal == correctAnswer){
      $('questionResult').text('Correct!');
      console.log("Correct!");
    } else{
      $('questionResult').text('Wrong!');
      console.log('Wrong!');
    }
}

grading();
