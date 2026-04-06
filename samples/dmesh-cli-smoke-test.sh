uv run dmesh reset --full
cat ./samples/dp1-minimal.yaml 
dpid=$(uv run dmesh put dp ./samples/dp1-minimal.yaml)
uv run dmesh get dp $dpid
cat ./samples/dc1-minimal.yaml
dcid=$(uv run dmesh put dc ./samples/dc1-minimal.yaml --dp $dpid)
uv run dmesh get dc $dcid