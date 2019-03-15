(function ($) {
    var $content_md = $('#div_id_content_md');
    var $content_ck = $('#div_id_content_ck');
    var $is_markdown = $('input[name=is_markdown]');
    var swith_editor = function (is_markdown) {
        if (is_markdown) {
            $content_md.show();
            $content_ck.hide();
        } else {
            $content_ck.show();
            $content_md.hide();
        }
    };
    $is_markdown.on('click', function () {
        swith_editor($(this).is(':checked'));
    });
    swith_editor($is_markdown.is(':checked'))
})(jQuery);