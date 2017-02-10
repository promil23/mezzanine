(function($) {
    'use strict';

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

//<<<<<<< HEAD

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
            autoresize_max_height: 400,
            link_list: '/displayable_links.js',
            relative_urls: false,
            convert_urls: false,
            menubar: false,
            statusbar: false,
            toolbar: ("insertfile undo redo | styleselect | bold italic | " +
                      "alignleft aligncenter alignright alignjustify | " +
                      "bullist numlist outdent indent | link image table | " +
                      "code fullscreen editprice edittip"),
            file_picker_callback: function (callback, value, meta) {
                myFilePicker(callback, value, meta);
            },
            image_class_list: [{'text': 'In gallery', 'value': 'img-responsive'}],
            content_css: window.__tinymce_css,
            content_style: "div.bct-price-component {display: inline-block;}",
            valid_elements: "*[*]",  // Don't strip anything since this is handled by bleach.
            force_br_newlines : true,
            force_p_newlines : false,
            //forced_root_block : false,
            //extended_valid_elements : 'span[price,currency,class]',
            extended_valid_elements : 'span[price|currency|class]',
            //extended_valid_elements : '*[*]',
            setup: function(ed) {
                ed.addButton('editprice', {
                            title : 'Edit price',
                            text: 'Edit price',
                            //image : 'img/example.gif',
                            icon: false,
                            onclick : function() {
                                ed.windowManager.open({
                                    title: 'Edit price',
                                    body: [
                                        {type: 'textbox', name: 'price', label: 'Price', value: ed.selection.getContent()}
                                    ],
                                    onsubmit: function(e) {    
                                        ed.focus();
                                        var price_arr = e.data.price.split(' ');
                                        var price = price_arr[0];
                                        var ccy_code = price_arr[1];
                                        var symbol = currencies[ccy_code];

                                        var content = 
                                        '<span class="bct-price-component">' + 
                                            '<span class="price" price="' + price + '">' + price + '</span><span class="ccy-symbol" currency="' + ccy_code + '">' + symbol + '</span>' + 
                                        '</span>';
                                        ed.selection.setContent(content);
                                    }
                                });
                            }
                });
                ed.addButton('edittip', {
                            title : 'Edit tip',
                            text: 'Edit tip',
                            icon: false,
                            onclick : function() {
                                var tipNumber = ed.selection.getContent().replace('[','').replace(']','');
                                ed.windowManager.open({
                                    title: 'Edit tip',
                                    body: [
                                        {type: 'textbox', name: 'tip', label: 'Tip number', value: tipNumber}
                                    ],
                                    onsubmit: function(e) {    
                                        ed.focus();
                                        var number = e.data.tip;
                                        var content = '[<a href="#tip-' + number + '">' + number + '</a>]';
                                        ed.selection.setContent(content);
                                    }
                                });
                            }
                });
            }
    };

    if (typeof tinyMCE != 'undefined') {

        tinyMCE.init(tinyMCEOptions);
    }
/*
=======
    function custom_file_browser(field_name, url, type, win) {
        tinyMCE.activeEditor.windowManager.open({
            title: 'Select ' + type + ' to insert',
            file: window.__filebrowser_url + '?pop=5&type=' + type,
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

    var tinymce_config = {
        height: '500px',
        language: language_codes[window.__language_code] || 'en',
        plugins: [
            "advlist autolink lists link image charmap print preview anchor",
            "searchreplace visualblocks code fullscreen",
            "insertdatetime media table contextmenu paste"
        ],
        link_list: window.__link_list_url,
        relative_urls: false,
        convert_urls: false,
        menubar: false,
        statusbar: false,
        toolbar: ("insertfile undo redo | styleselect | bold italic | " +
                  "alignleft aligncenter alignright alignjustify | " +
                  "bullist numlist outdent indent | link image table | " +
                  "code fullscreen"),
        file_browser_callback: custom_file_browser,
        content_css: window.__tinymce_css,
        valid_elements: "*[*]"  // Don't strip anything since this is handled by bleach.
    };

    function initialise_richtext_fields($elements) {
        if ($elements && typeof tinyMCE != 'undefined') {
            $elements.tinymce(tinymce_config);
        }
    }

    // Register a handler for Django's formset:added event, to initialise
    // any rich text fields in dynamically added inline forms.
    $(document).on('formset:added', function(e, $row) {
        initialise_richtext_fields($row.find('textarea.mceEditor'));
    });
>>>>>>> upstream/master
*/

    // Initialise all existing editor fields, except those with an id
    // containing the string "__prefix__". Those elements are part of the
    // hidden template inline rows used by Django's dynamic inlines, and they
    // shouldn't be initialised as editors.
    $(document).ready(function() {
        initialise_richtext_fields($('textarea.mceEditor').filter(function() {
            return (this.id || '').indexOf('__prefix__') === -1;
        }));
    });

})(window.django ? django.jQuery : jQuery);
