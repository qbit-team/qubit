/**
 * @license Copyright (c) 2003-2018, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	//config.contentsLangDirection = "rtl";
    config.removeButtons = 'About,Save,Form,Flash,Button,ImageButton,Iframe,CreateDiv,Checkbox,Radio,Textarea,TextField,Select,HiddenField';
    config.mathJaxLib = '//cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-AMS_HTML';
    //config.language = 'fa';
    config.extraPlugins = 'codesnippet';
    config.extraPlugins = 'mathjax';

};
