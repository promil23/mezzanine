
// Map Django language codes to valid TinyMCE language codes.
// There's an entry for every TinyMCE language that exists,
// so if a Django language code isn't here, we can default to en.

var language_codes = {
    'ar': 'ar',
    'ca': 'ca',
    'cs': 'cs',
    'da': 'da',
    'de': 'de',
    'es': 'es',
    'et': 'et',
    'fa': 'fa',
    'fa-ir': 'fa_IR',
    'fi': 'fi',
    'fr': 'fr_FR',
    'hr-hr': 'hr',
    'hu': 'hu_HU',
    'id-id': 'id',
    'is-is': 'is_IS',
    'it': 'it',
    'ja': 'ja',
    'ko': 'ko_KR',
    'lv': 'lv',
    'nb': 'nb_NO',
    'nl': 'nl',
    'pl': 'pl',
    'pt-br': 'pt_BR',
    'pt-pt': 'pt_PT',
    'ru': 'ru',
    'sk': 'sk',
    'sr': 'sr',
    'sv': 'sv_SE',
    'tr': 'tr',
    'uk': 'uk_UA',
    'vi': 'vi',
    'zh-cn': 'zh_CN',
    'zh-tw': 'zh_TW',
    'zh-hant': 'zh_TW',
    'zh-hans': 'zh_CN'
};

/*
function custom_file_browser(field_name, url, type, win) {
    tinyMCE.activeEditor.windowManager.open({
        title: 'Select ' + type + ' to insert',
        file: window.__filebrowser_url + '?pop=2&file=' + type,
        width: 800,
        height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'yes',
        close_previous: 'no'
    }, {
        window: win,
        input: field_name
    });
    return false;
}
*/

function myFilePicker(callback, value, meta) {

    //var cmsURL = '/admin/filebrowser/browse/?pop=2';
    //cmsURL = cmsURL + '&type=' + type;
    var cmsURL = window.__filebrowser_url + '?pop=2' + '&type=' + meta.filetype;

    tinyMCE.activeEditor.windowManager.open({
        file: cmsURL,
        //width: 980,  // Your dimensions may differ - toy around with them!
        //height: 500,
        resizable: 'yes',
        scrollbars: 'yes',
        inline: 'no',  // This parameter only has an effect if you use the inlinepopups plugin!
        close_previous: 'no',
    }, {
        //window: win,
        //input: field_name,
        oninsert: function (url) {
            callback(url);
        }
    });
    return false;
}


grp.jQuery(function($) {
    tinyMCEOptions = {
            selector: 'textarea.mceEditor:not([name*="__prefix__"])',
            //height: '500px',
            width: '100%',
            language: language_codes[window.__language_code] || 'en',
            plugins: [
                "advlist autolink autoresize, lists link image charmap print preview anchor",
                "searchreplace visualblocks code fullscreen",
                "insertdatetime media table contextmenu paste"
            ],
            link_list: '/displayable_links.js',
            relative_urls: false,
            convert_urls: false,
            menubar: false,
            statusbar: false,
            toolbar: ("insertfile undo redo | styleselect | bold italic | " +
                      "alignleft aligncenter alignright alignjustify | " +
                      "bullist numlist outdent indent | link image table | " +
                      "code fullscreen"),
            file_picker_callback: function (callback, value, meta) {
                myFilePicker(callback, value, meta);
            },
            image_class_list: [{'text': 'In gallery', 'value': 'img-responsive'}],
            content_css: window.__tinymce_css,
            valid_elements: "*[*]"  // Don't strip anything since this is handled by bleach.
    };

    if (typeof tinyMCE != 'undefined') {

        tinyMCE.init(tinyMCEOptions);

    }

});
