uv run dmesh reset --full
Get-Content ./examples/dp1-minimal.yaml
$dpid = uv run dmesh put dp ./examples/dp1-minimal.yaml
uv run dmesh get dp $dpid
Get-Content ./examples/dc1-minimal.yaml
$dcid = uv run dmesh put dc ./examples/dc1-minimal.yaml --dp-id $dpid
uv run dmesh get dc $dcid
