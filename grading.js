function grading(){
    var points = 0;
    var radioVal = $("input[name='quiz']:checked").val();
    var textVal = $("input[name='quiz'][type='text']").val();
    var correctAnswer = $('p').attr('data-answer');
    if (radioVal == correctAnswer || textVal == correctAnswer){
      $('questionResult').text('Correct!');
    } else{
      $('questionResult').text('Wrong!');
    }
}
