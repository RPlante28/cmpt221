function validateForm() {
    // create a regex expression to ensure input only contains letters
    var firstNameRe = newRegExp("^[A-Za-z]+$");
    // get the value submitted in the first name field in the sign up form
    let firstName = document.forms["SignUp"]["FirstName"].value;

    // test to see if the input matches the regex pattern
    if (!firstNameRe.test(firstName)) {
        // if it does not match the pattern,
        // alert the user and do not accept the input
        alert("Name can only contain letters.");
        return false;
    }
}