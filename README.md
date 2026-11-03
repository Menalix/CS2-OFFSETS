# CS2 Offsets

Public Counter-Strike 2 offsets and schema fields from [Hexui](https://hexui.com/offsets/).

JSON files mirror the latest successfully published Hexui dump. Updates are checked every 30 minutes; a game update may need additional validation before a new dump is published. See [metadata.json](metadata.json) for the exported build and Steam manifest.

`offsets.json` contains signature-derived addresses and member offsets. The `*.dll.json` files contain named schema classes and fields. Values are decimal byte offsets or module-relative addresses.

Some signature names use Hexui's internal naming conventions and may differ from other dumpers. They describe our usage of the resolved value, rather than an official Valve symbol. Schema names come from the game's compiled descriptors.

## API

Use [hexui.com/offsets/](https://hexui.com/offsets/) to browse modules, search symbols and select only the fields you need. Click **Generate API link** to get a reusable JSON URL that follows the latest published dump.

- [Complete JSON API](https://hexui.com/offsets/api/)
- [Signature offsets JSON](https://hexui.com/offsets/api/?file=offsets)
- [Client schema JSON](https://hexui.com/offsets/api/?file=client.dll)

API requests are limited to one per IP every 10 seconds. Generated selection links expire after 30 days without a successful request. If a selected symbol disappears after an update, the API returns an error instead of an older value.
