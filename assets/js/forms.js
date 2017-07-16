
function initDatePicker($element, langCode, useCurrent, initialDate, $form, $input) {
    var options = {
        format: 'L',
        locale: langCode,
        useCurrent: useCurrent
    };
    if (initialDate){
        initialDate = moment(initialDate);
        options['defaultDate'] = initialDate;
    }
    $element.datetimepicker(options);
    $form.on('submit', function () {
        var selectedDate = element.data('DateTimePicker').date();
        if (selectedDate){
            $input.attr('value', selectedDate.format('YYYY-MM-DD'))
        }
    });
    return initialDate
}

function initLinkedDatePickers($datePickerStart, $datePickerEnd, $form, initialDateStart, initialDateEnd, langCode) {
    var $inputStart = $datePickerStart.find('input:first-child'),
        $inputEnd = $datePickerEnd.find('input:first-child');

    initialDateStart = initDatePicker($datePickerStart, langCode, true, initialDateStart, $form, $inputStart);
    initialDateEnd = initDatePicker($datePickerEnd, langCode, false, initialDateEnd, $form, $inputEnd);

    if (initialDateStart){
        $datePickerEnd.data('DateTimePicker').minDate(initialDateStart)
    }

    if (initialDateEnd){
        $datePickerStart.data('DateTimePicker').maxDate(initialDateEnd)
    }

    $datePickerStart.on("dp.change", function (e) {
        $datePickerEnd.data("DateTimePicker").minDate(e.date);
    });

    $datePickerEnd.on("dp.change", function (e) {
        $datePickerStart.data("DateTimePicker").maxDate(e.date);
    });
}