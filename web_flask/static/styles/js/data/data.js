function retrive_data(ur){
    console.log(ur)
    //use jquery
    var data = [];
    $.ajax({
      url: ur,
      type: 'GET',
      async: false,
      success: function(response){
        data = response;
      }
    });
    return data;
  }

  export {retrive_data};