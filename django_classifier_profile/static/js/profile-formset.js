$(function() {
    var totalForms = $('#id_form-TOTAL_FORMS');

    $('.formset-btn-add-form').click(function() {
        var $btn = $(this);
        var emptyForm = $('#empty-form-' + $btn.data('group'));
        var index = parseInt(totalForms.val(), 10);

        $btn.parent().find('.formset-forms').append(
            emptyForm.html().replace(/__prefix__/g, index)
        );

        totalForms.val(index + 1);
    });

    $(document).on('click', '.formset-btn-delete', function() {
        var $btn = $(this);
        $btn.parent().find('input[name$=DELETE]').prop('checked', true);
        $btn.parents('.form-user-attribute').hide();
    });
});
