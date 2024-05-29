import "./chunk-EX6ADWAR.mjs";

// src/resolver.ts
import { toArray, uniq } from "@antfu/utils";
import { camelToKebab } from "@iconify/utils/lib/misc/strings";

// src/core/icon-sets.json
var icon_sets_default = [
  "academicons",
  "akar-icons",
  "ant-design",
  "arcticons",
  "basil",
  "bi",
  "bpmn",
  "brandico",
  "bx",
  "bxl",
  "bxs",
  "bytesize",
  "carbon",
  "charm",
  "ci",
  "cib",
  "cif",
  "cil",
  "circle-flags",
  "circum",
  "clarity",
  "codicon",
  "covid",
  "cryptocurrency",
  "cryptocurrency-color",
  "dashicons",
  "devicon",
  "devicon-plain",
  "ei",
  "el",
  "emojione",
  "emojione-monotone",
  "emojione-v1",
  "entypo",
  "entypo-social",
  "eos-icons",
  "ep",
  "et",
  "eva",
  "fa",
  "fa-brands",
  "fa-regular",
  "fa-solid",
  "fa6-brands",
  "fa6-regular",
  "fa6-solid",
  "fad",
  "fe",
  "feather",
  "file-icons",
  "flag",
  "flagpack",
  "flat-color-icons",
  "flat-ui",
  "fluent",
  "fluent-emoji",
  "fluent-emoji-flat",
  "fluent-emoji-high-contrast",
  "fluent-mdl2",
  "fontelico",
  "fontisto",
  "formkit",
  "foundation",
  "fxemoji",
  "gala",
  "game-icons",
  "geo",
  "gg",
  "gis",
  "gridicons",
  "grommet-icons",
  "guidance",
  "healthicons",
  "heroicons",
  "heroicons-outline",
  "heroicons-solid",
  "humbleicons",
  "ic",
  "icomoon-free",
  "icon-park",
  "icon-park-outline",
  "icon-park-solid",
  "icon-park-twotone",
  "iconamoon",
  "iconoir",
  "icons8",
  "il",
  "ion",
  "iwwa",
  "jam",
  "la",
  "line-md",
  "logos",
  "ls",
  "lucide",
  "majesticons",
  "maki",
  "map",
  "material-symbols",
  "mdi",
  "mdi-light",
  "medical-icon",
  "memory",
  "mi",
  "mingcute",
  "mono-icons",
  "nimbus",
  "nonicons",
  "noto",
  "noto-v1",
  "octicon",
  "oi",
  "ooui",
  "openmoji",
  "pajamas",
  "pepicons",
  "pepicons-pencil",
  "pepicons-pop",
  "pepicons-print",
  "ph",
  "pixelarticons",
  "prime",
  "ps",
  "quill",
  "radix-icons",
  "raphael",
  "ri",
  "si-glyph",
  "simple-icons",
  "simple-line-icons",
  "skill-icons",
  "solar",
  "streamline",
  "streamline-emojis",
  "subway",
  "svg-spinners",
  "system-uicons",
  "tabler",
  "tdesign",
  "teenyicons",
  "topcoat",
  "twemoji",
  "typcn",
  "uil",
  "uim",
  "uis",
  "uit",
  "uiw",
  "vaadin",
  "vs",
  "vscode-icons",
  "websymbol",
  "whh",
  "wi",
  "wpf",
  "zmdi",
  "zondicons"
];

// src/resolver.ts
function ComponentsResolver(options = {}) {
  var _a;
  const {
    prefix: rawPrefix = (_a = options.componentPrefix) != null ? _a : "i",
    enabledCollections = icon_sets_default,
    alias = {},
    customCollections = [],
    extension
  } = options;
  const prefix = rawPrefix ? `${camelToKebab(rawPrefix)}-` : "";
  const ext = extension ? extension.startsWith(".") ? extension : `.${extension}` : "";
  const collections = uniq([
    ...toArray(enabledCollections),
    ...toArray(customCollections),
    ...toArray(Object.keys(alias))
  ]);
  collections.sort((a, b) => b.length - a.length);
  return (name) => {
    const kebab = camelToKebab(name);
    if (!kebab.startsWith(prefix))
      return;
    const slice = kebab.slice(prefix.length);
    const collection = collections.find((i) => slice.startsWith(`${i}-`)) || collections.find((i) => slice.startsWith(i));
    if (!collection)
      return;
    let icon = slice.slice(collection.length);
    if (icon[0] === "-")
      icon = icon.slice(1);
    if (!icon)
      return;
    const resolvedCollection = alias[collection] || collection;
    if (collections.includes(resolvedCollection))
      return `~icons/${resolvedCollection}/${icon}${ext}`;
  };
}
export {
  ComponentsResolver as default
};
