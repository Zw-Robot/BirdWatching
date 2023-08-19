import { request } from "./request"

export async function create_bird(params: any) {
  const res = await request.post("/inventory/create_bird", params);
  return res.data;
}
export async function update_bird(params: any) {
  const res = await request.post("/inventory/update_bird", params);
  return res.data;
}
export async function delete_bird(params: any) {
  const res = await request.get("/inventory/delete_bird", params);
  return res.data;
}
export async function get_all_birds(params: any) {
  const res = await request.get("/inventory/get_all_birds", params);
  return res.data;
}
export async function get_all_orders(params: any={}) {
  const res = await request.get("/inventory/get_all_orders", params);
  return res.data;
}
export async function wx_get_all_birds(params: any = {}) {
  const res = await request.get("/inventory/wx_get_all_birds", params);
  return res.data;
}
export async function get_bird(params: any) {
  const res = await request.get("/inventory/get_bird", params);
  return res.data;
}
export async function create_bird_survey(params: any) {
  const res = await request.post("/inventory/create_bird_survey", params);
  return res.data;
}
export async function update_bird_survey(params: any) {
  const res = await request.post("/inventory/update_bird_survey", params);
  return res.data;
}
export async function delete_bird_survey(params: any) {
  const res = await request.get("/inventory/delete_bird_survey", params);
  return res.data;
}
export async function get_all_bird_surveys(params: any) {
  const res = await request.get("/inventory/get_all_bird_surveys", params);
  return res.data;
}
export async function get_bird_survey(params: any) {
  const res = await request.get("/inventory/get_bird_survey", params);
  return res.data;
};
export async function create_bird_record(params: any) {
  const res = await request.post("/inventory/create_bird_record", params);
  return res.data;
};
export async function update_bird_record(params: any) {
  const res = await request.post("/inventory/update_bird_record", params);
  return res.data;
};
export async function delete_bird_record(params: any) {
  const res = await request.get("/inventory/delete_bird_record", params);
  return res.data;
};
export async function get_all_bird_records(params: any) {
  const res = await request.get("/inventory/get_all_bird_records", params);
  return res.data;
};
export async function get_bird_record(params: any) {
  const res = await request.get("/inventory/get_bird_record", params);
  return res.data;
};
export async function create_match(params: any) {
  const res = await request.post("/competition/create_match", params);
  return res.data;
};
export async function update_match(params: any) {
  const res = await request.post("/competition/update_match", params);
  return res.data;
};
export async function get_all_matches(params: any) {
  const res = await request.get("/competition/get_all_matches", params);
  return res.data;
};
export async function delete_match(params: any) {
  const res = await request.get("/competition/delete_match", params);
  return res.data;
};
export async function create_group(params: any) {
  const res = await request.post("/competition/create_group", params);
  return res;
};
export async function add_group(params: any) {
  const res = await request.post("/competition/add_group", params);
  return res;
};
export async function update_group(params: any) {
  const res = await request.post("/competition/update_group", params);
  return res.data;
};
export async function delete_group(params: any) {
  const res = await request.post("/competition/delete_group", params);
  return res.data;
};
export async function get_all_groups(params: any) {
  const res = await request.get("/competition/get_all_groups", params);
  return res.data;
};
export async function wx_post_base64(params: any) {
  const res = await request.post("/inventory/wx_post_base64", params);
  return res.data;
};

export async function sgin(params: any) {
  const res = await request.post("/auth/sgin", params);
  return res.data;
};

export async function info(params: any) {
  const res = await request.post("/auth/info", params);
  return res.data;
};