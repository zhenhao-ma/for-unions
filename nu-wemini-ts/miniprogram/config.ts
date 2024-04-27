export const config: IConfig = {
  API_PREFIX: 'http://127.0.0.1:8000/api/v1',
  COUNTRIES: [
    {
      id: "US" as Country.US,
      name: "US"
    },
    {
      id: "CN" as Country.CN,
      name: "CN"
    },
    {
      id: "UK" as Country.UK,
      name: "UK"
    }
  ],
  CONNECT_TYPES: [
    {
      id: "REQUIRE_APPROVE" as ConnectType.REQUIRE_APPROVE,
      name: "经同意后可查看你的资料"
    },
    {
      id: "OPEN" as ConnectType.OPEN,
      name: "可直接查看你的资料"
    },
    {
      id: "CLOSED" as ConnectType.CLOSED,
      name: "隐藏全部资料"
    }
  ]
}