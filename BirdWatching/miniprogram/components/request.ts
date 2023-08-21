class Request{
  private URL:string = "http://43.138.33.82:5500"
  get(url: string, params: any): Promise<any> {
    const join_url = this.URL + url;
    return new Promise((resolve, reject) => {
      wx.request({
        method: "GET",
        url: join_url,
        data: params,
        header: { "content-type": "application/json" },
        success(res) {
          resolve(res.data);
        },
        fail(error) {
          reject(error);
        },
      });
    });
  }
  post(url: string, data: any): Promise<any> {
    const join_url = this.URL + url;
    return new Promise((resolve, reject) => {
      wx.request({
        method: "POST",
        url: join_url,
        data: data,
        header: { "content-type": "application/json" },
        success(res) {
          resolve(res.data);
        },
        fail(error) {
          reject(error);
        },
      });
    });
  }
}
export let request = new Request()