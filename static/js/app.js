


window.onload = function (){

    const queryString = window.location.search;
    console.log(queryString);
    const urlParams = new URLSearchParams(queryString);
    const dim = urlParams.get('dim')
    console.log(dim);

    const element = "q_" + dim
    const q_ = document.getElementById(element); // results
    q_.style.display = "block";
    console.log(dim);


    //
    // if(dim == 1){
    //      const q_0 = document.getElementById("q_0");
    //      const q_1 = document.getElementById("q_1"); // results
    //      q_1.style.display = "block";
    //      console.log(dim);
    // }

}






