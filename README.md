# CS2 Offsets

Public Counter-Strike 2 offsets and schema fields from [Hexui](https://hexui.com/offsets/).

JSON files mirror the latest successfully published Hexui dump. Updates are checked every 30 minutes (GitHub may delay scheduled runs); a game update may need additional validation before a new dump is published. See [metadata.json](metadata.json) for the exported build and Steam manifest.

- `offsets.json`: signature-derived addresses and member offsets.
- `buttons.json`: button-state addresses, using names such as `attack`, `jump` and `use`.
- `interfaces.json`: verified static interface singleton addresses, grouped by DLL.
- `*.dll.json`: compact named schema classes and field offsets, including `worldrenderer.dll`.

Values are decimal byte offsets or module-relative addresses extracted from the exact downloaded game build. Runtime-created interfaces without a verified static singleton are omitted. These compact numeric exports do not include rich schema type/enum metadata.

Some signature names use Hexui's internal naming conventions and may differ from other dumpers. They describe our usage of the resolved value, rather than an official Valve symbol. Schema names come from the game's compiled descriptors.

## API

Use [hexui.com/offsets/](https://hexui.com/offsets/) to browse modules, search symbols and select only the fields you need. Click **Generate API link** to get a reusable JSON URL that follows the latest published dump.

- [Complete JSON API](https://hexui.com/offsets/api/)
- [Signature offsets JSON](https://hexui.com/offsets/api/?file=offsets)
- [Buttons JSON](https://hexui.com/offsets/api/?file=buttons)
- [Interfaces JSON](https://hexui.com/offsets/api/?file=interfaces)
- [Client schema JSON](https://hexui.com/offsets/api/?file=client.dll)

Full API exports allow one request per IP every 0.5 seconds. Generated selection links allow one every 5 seconds and expire after 7 days without a successful request. If a selected symbol disappears after an update, the API returns an error instead of an older value.
