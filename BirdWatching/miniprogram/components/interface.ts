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
export async function get_bird(params: any) {
  const res = await request.get("/inventory/get_bird", params);
  return res.data;
}
export async function creatBirdSearch(params: any) {
  const res = await request.post("/inventory/create_bird_survey", params);
  return res.data;
}
export async function updataBirdSearch(params: any) {
  const res = await request.post("/inventory/update_bird_survey", params);
  return res.data;
}
export async function delateBirdSearch(params: any) {
  const res = await request.get("/inventory/delete_bird_survey", params);
  return res.data;
}
export async function getAllBirdSearch(params: any) {
  const res = await request.get("/inventory/get_all_bird_surveys", params);
  return res.data;
}
export async function findBirdSearch(params: any) {
  const res = await request.get("/inventory/get_bird_survey", params);
  return res.data;
};
export async function creatBirdRecording(params: any) {
  const res = await request.post("/inventory/create_bird_record", params);
  return res.data;
};
export async function updataBirdRecording(params: any) {
  const res = await request.post("/inventory/update_bird_record", params);
  return res.data;
};
export async function delateBirdRecording(params: any) {
  const res = await request.get("/inventory/delete_bird_record", params);
  return res.data;
};
export async function getAllBirdRecording(params: any) {
  const res = await request.get("/inventory/get_all_bird_records", params);
  return res.data;
};
export async function getOneBirdRecording(params: any) {
  const res = await request.get("/inventory/get_bird_record", params);
  return res.data;
};