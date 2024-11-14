// import globals from "globals";
// import pluginJs from "@eslint/js";


// /** @type {import('eslint').Linter.Config[]} */
// export default [
//  {files: ["**/*.html"],
//    languageOptions: {
//      sourceType: "script"}},
//  {languageOptions: { globals: globals.browser }},
//  pluginJs.configs.recommended,
//];

import globals from "globals";
import pluginJs from "@eslint/js";
import pluginHtml from "eslint-plugin-html";

/** @type {import('eslint').Linter.Config[]} */
export default [
  {
    // This targets my custom HTML files.
    // I'm not interested in the Django files copied into my project.
    files: ["shopping_list/templates/*.html"], 
    languageOptions: {
      globals: {
        bootstrap: "readonly", // eslint ain't familiar with bootstrap
        $: "readonly", // eslint doesn't know about jQuery
        ...globals.browser,
      },
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "script", // Treat the files as non-modular scripts
      },
    },
    plugins:  {
      html: pluginHtml,
    },

    rules: {
      // Three custom rules:
      // eslint doesn't see the use of toggleCancelUncancel, but my shopping_list.html file does!
      "no-unused-vars": ["error", { "varsIgnorePattern": "toggleCancelUncancel" }],
      // Lines should be no longer than 80 characters.
      "max-len": ["error", { "code": 79 }],
      // Indents should be small and uniform.
      "indent": ["error", 4]
    },
  },
  pluginJs.configs.recommended,
];