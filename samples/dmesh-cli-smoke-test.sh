uv run dmesh reset --full
cat ./sandbox/dp1.yaml 
dpid=$(uv run dmesh put dp ./sandbox/dp1.yaml)
uv run dmesh get dp $dpid
cat ./sandbox/dc1.yaml
dcid=$(uv run dmesh put dc ./sandbox/dc1.yaml --dp $dpid)
uv run dmesh get dc $dcid