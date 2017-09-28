/**
 * Created by mammu on 20.02.2017.
 */
var calculated = false;

function add(num1, num2) {
    return num1 + num2;
}

function subtract(num1, num2) {
    return num1 - num2;
}

function multiply(num1, num2) {
    return num1 * num2;
}

function divide(num1, num2) {
    return num1 / num2;
}

function clearInput() {
    $("#textBox").val("");
}

function addToInput(value) {
    var text = $("#textBox").val();
    var symbols = ["+", "-", "*", "/"];

    if ($.inArray(value, symbols) != -1 && !calculated) {
        if (text != "" && text.indexOf(" ") == -1) {
            text += " " + value + " ";
        }
    } else if (calculated) {
        text = value;
        calculated = false;
    } else {
        text += value;
    }
    $("#textBox").val(text);
}

function calculate() {
    var text = $("#textBox").val();

    if (text.indexOf(" ") != -1) {
        var equation = text.split(" ");
        var num1 = parseInt(equation[0]);
        var num2 = parseInt(equation[2]);
        var result;
        if (equation[1] == "+") {
            result = add(num1, num2);
        } else if (equation[1] == "-") {
            result = subtract(num1, num2);
        } else if (equation[1] == "*") {
            result = multiply(num1, num2);
        } else {
            result = divide(num1, num2);
        }
        calculated = true;
        $("#textBox").val(result);
    }
}
