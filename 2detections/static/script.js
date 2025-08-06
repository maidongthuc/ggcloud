let capturedImages = [];

let currentImageIndex = -1;

const previewImage = document.getElementById("preview-image");
const btnPrev = document.getElementById("prev-btn");
const btnNext = document.getElementById("next-btn");
const btnAnalyze6S = document.getElementById("btn-analyze-6s");
const loading = document.getElementById("loading");
const resultBox = document.getElementById("analysis-result");
const previewTitle = document.querySelector(".image-preview-section h3");
const btnReset = document.getElementById("btn-reset");
const btnAnalyzeEC = document.getElementById("btn-analyze-ec");

const btnCheckList = document.getElementById("btn-check_list");
const checklistForm = document.getElementById("checklist-form");

// ...existing code...

const btnAnalyzeChecklist = document.getElementById("btn-analyze-checklist");

function displayChecklistResult(result) {
  resultBox.innerHTML = ""; // Xóa nội dung cũ

  // Ảnh đầu tiên (nếu có)
  let firstImg = null;
  if (result.url_image) {
    if (Array.isArray(result.url_image)) {
      if (result.url_image.length > 0) firstImg = result.url_image[0];
    } else if (typeof result.url_image === "string" && result.url_image) {
      firstImg = result.url_image;
    }
  }
  if (firstImg) {
    const img = document.createElement("img");
    img.src = firstImg;
    img.alt = "Checklist main image";
    img.style.display = "block";
    img.style.margin = "0 auto 16px auto";
    img.style.maxWidth = "320px";
    img.style.maxHeight = "220px";
    img.style.objectFit = "contain";
    resultBox.appendChild(img);
  }

  // Tiêu đề
  const title = document.createElement("h4");
  title.textContent = "Kết quả phân tích Checklist";
  title.style.color = "#1e3a8a";
  resultBox.appendChild(title);

  // Ảnh (nếu có, hiển thị tất cả)
  if (result.url_image && Array.isArray(result.url_image) && result.url_image.length > 0) {
    const imgRow = document.createElement("div");
    imgRow.style.display = "flex";
    imgRow.style.gap = "12px";
    imgRow.style.margin = "12px 0";
    result.url_image.forEach((imgUrl) => {
      const img = document.createElement("img");
      img.src = imgUrl;
      img.alt = "Checklist result image";
      img.style.maxWidth = "220px";
      img.style.maxHeight = "180px";
      img.style.objectFit = "contain";
      img.loading = "lazy";
      imgRow.appendChild(img);
    });
    resultBox.appendChild(imgRow);
  }

  // Kết quả và lý do
  const resultDiv = document.createElement("div");
  resultDiv.style.background = "#f1f5f9";
  resultDiv.style.border = "1px solid #cbd5e1";
  resultDiv.style.borderRadius = "8px";
  resultDiv.style.padding = "16px";
  resultDiv.style.marginTop = "8px";
  resultDiv.style.fontSize = "1.08rem";
  resultDiv.innerHTML = `
    <b>Kết quả:</b> <span style="color:#16a34a">${result.result || "-"}</span><br>
    <b>Nhận xét:</b> ${result.reason || "-"}
  `;
  resultBox.appendChild(resultDiv);
}





btnAnalyzeChecklist.addEventListener("click", async () => {
  if (capturedImages.length === 0) {
    alert("Chưa có ảnh nào để phân tích.");
    return;
  }

  // Lấy nội dung 3 ô nhập
  const inspectionLocation = document.getElementById("inspection-location").value;
  const inspectionItems = document.getElementById("inspection-items").value;
  const inspectionMethods = document.getElementById("inspection-methods").value;

  loading.style.display = "block";
  resultBox.innerHTML = "";

  try {
    const formData = new FormData();
    for (let i = 0; i < capturedImages.length; i++) {
      const dataUrl = capturedImages[i];
      const blob = await (await fetch(dataUrl)).blob();
      const file = new File([blob], `image_${i + 1}.jpg`, { type: "image/jpeg" });
      formData.append("files", file);
    }
    formData.append("inspection_location", inspectionLocation);
    formData.append("inspection_items_details", inspectionItems);
    formData.append("inspection_methods_standards", inspectionMethods);

    const res = await fetch("/api/v1/check_list/check_list/", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error("Phân tích checklist thất bại: " + res.statusText);
    }

    const result = await res.json();
    loading.style.display = "none";

    // Hiển thị kết quả ra resultBox (tùy backend trả về, bạn có thể chỉnh lại cho đẹp)
    displayChecklistResult(result);
    previewTitle.textContent = "Result Images";
  } catch (err) {
    loading.style.display = "none";
    console.error("Lỗi phân tích checklist:", err);
    alert("Lỗi khi gọi API check_list: " + (err.message || err));
  }
});
// ...existing code...

btnCheckList.addEventListener("click", () => {
  if (checklistForm.style.display === "none") {
    checklistForm.style.display = "block";
  } else {
    checklistForm.style.display = "none";
  }
});

function updatePreview() {
  const previewImage = document.getElementById("preview-image");
  const imageCounter = document.getElementById("image-counter");
  const btnPrev = document.getElementById("prev-btn");
  const btnNext = document.getElementById("next-btn");

  const total = capturedImages.length;

  if (total === 0) {
    previewImage.src = "";
    previewImage.alt = "Chưa có ảnh";
    imageCounter.textContent = "0 / 0";
    btnPrev.style.visibility = "hidden";
    btnNext.style.visibility = "hidden";
    return;
  }

  previewImage.src = capturedImages[currentImageIndex];
  imageCounter.textContent = `${currentImageIndex + 1} / ${total}`;

  // Hiển thị nút khi có từ 2 ảnh trở lên
  if (total > 1) {
    btnPrev.style.visibility = "visible";
    btnNext.style.visibility = "visible";
  } else {
    btnPrev.style.visibility = "hidden";
    btnNext.style.visibility = "hidden";
  }
}


// Prev/Next
btnPrev.addEventListener("click", () => {
  if (capturedImages.length === 0) return;
  currentImageIndex = (currentImageIndex - 1 + capturedImages.length) % capturedImages.length;
  updatePreview();
});

btnNext.addEventListener("click", () => {
  if (capturedImages.length === 0) return;
  currentImageIndex = (currentImageIndex + 1) % capturedImages.length;
  updatePreview();
});

document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const btnCapture = document.getElementById("btn-capture");

  // Bắt đầu hiển thị camera sau
  async function initCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: "environment" } }, // camera sau
        audio: false,
      });
      video.srcObject = stream;
    } catch (err) {
      alert("Can not access to the camera: " + err.message);
    }
  }

  initCamera();

  // Sự kiện khi bấm "Chụp ảnh"
// ...existing code...
btnCapture.addEventListener("click", async () => {
  const context = canvas.getContext("2d");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  context.drawImage(video, 0, 0, canvas.width, canvas.height);

  // Lấy ảnh local, không upload
  const dataUrl = canvas.toDataURL("image/jpeg");
  capturedImages.push(dataUrl);

  // Luôn chuyển đến ảnh mới nhất sau khi chụp
  currentImageIndex = capturedImages.length - 1;
  updatePreview();
});
// ...existing code...
});
function displayFireExtinguisherResults(results) {
  resultBox.innerHTML = ""; // Xóa nội dung cũ
  results.forEach(item => {
  // Lấy danh sách ảnh (có thể là mảng hoặc chuỗi)
  let images = [];
  if (item.result && item.result.url_image) {
    if (Array.isArray(item.result.url_image)) {
      images = item.result.url_image;
    } else if (typeof item.result.url_image === "string") {
      images = [item.result.url_image];
    }
  }
  // clock có thể là mảng các object
  if (item.type === "clock" && Array.isArray(item.result)) {
    images = item.result.map(r => r.url_image).filter(Boolean);
  }

  // Tạo wrapper cho mỗi vùng
  const wrapper = document.createElement("div");
  wrapper.style.marginBottom = "24px";
  wrapper.style.borderBottom = "1px solid #eee";
  wrapper.style.paddingBottom = "16px";

  // Hiển thị tất cả ảnh theo chiều ngang
  if (images.length > 0) {
    const imgRow = document.createElement("div");
    imgRow.style.display = "flex";
    imgRow.style.gap = "12px";
    imgRow.style.marginBottom = "10px";
    images.forEach((imgUrl) => {
      const img = document.createElement("img");
      img.src = imgUrl;
      img.alt = `${item.type} result image`;
      img.style.maxWidth = "220px";
      img.style.maxHeight = "180px";
      img.style.objectFit = "contain";
      img.loading = "lazy";
      imgRow.appendChild(img);
    });
    wrapper.appendChild(imgRow);
  }

  // Tiêu đề loại vùng
  const title = document.createElement("h4");
  title.textContent = `🔹 ${item.type.toUpperCase()}`;
  title.style.color = "#1e3a8a";
  wrapper.appendChild(title);

  // Thông tin phân tích (chỉ 1 lần, không lặp theo ảnh)
  const info = document.createElement("div");
  info.style.fontSize = "1rem";
  info.style.marginBottom = "6px";

  if (item.type === "clock" && Array.isArray(item.result)) {
    // Nếu clock là mảng, hiển thị từng info cho từng ảnh
    item.result.forEach((clockResult, idx) => {
      info.innerHTML += `
        <b>Đồng hồ #${idx + 1}:</b><br>
        <b>Status:</b> ${clockResult.status || "-"}<br>
        <b>Reason:</b> ${clockResult.reason || "-"}<br><br>
      `;
    });
  } else if (item.type === "tray" && item.result) {
    info.innerHTML = `
      <b>Tray Condition:</b> ${item.result.tray_condition?.status || "-"} - ${item.result.tray_condition?.reason || ""}<br>
      <b>Capacity:</b> ${item.result.capacity?.status || "-"} - ${item.result.capacity?.reason || ""}<br>
      <b>Cleanliness:</b> ${item.result.cleanliness?.status || "-"} - ${item.result.cleanliness?.reason || ""}
    `;
  } else if (item.result) {
    info.innerHTML = `
      <b>Body:</b> ${item.result.body?.status || "-"} - ${item.result.body?.reason || ""}<br>
      <b>Handle:</b> ${item.result.handle?.status || "-"} - ${item.result.handle?.reason || ""}<br>
      <b>Safety Pin:</b> ${item.result.safety_pin?.status || "-"} - ${item.result.safety_pin?.reason || ""}<br>
      <b>Nozzle:</b> ${item.result.nozzle?.status || "-"} - ${item.result.nozzle?.reason || ""}<br>
      <b>Cleanliness:</b> ${item.result.cleanliness?.status || "-"} - ${item.result.cleanliness?.reason || ""}
    `;
  }
  wrapper.appendChild(info);

  resultBox.appendChild(wrapper);
});
}

function displayFireCabinet5SResult(result) {
  resultBox.innerHTML = "<h4>Kết quả đánh giá 5S tủ chữa cháy:</h4>";
  const table = document.createElement("table");
  table.style.width = "100%";
  table.style.borderCollapse = "collapse";
  table.style.marginTop = "8px";

  Object.entries(result).forEach(([key, value]) => {
    const row = document.createElement("tr");

    // Tiêu chí
    const tdKey = document.createElement("td");
    tdKey.textContent = key.toUpperCase();
    tdKey.style.fontWeight = "bold";
    tdKey.style.padding = "6px 8px";
    tdKey.style.width = "110px";
    tdKey.style.borderBottom = "1px solid #eee";

    // Trạng thái
    const tdStatus = document.createElement("td");
    tdStatus.textContent = value.status;
    tdStatus.style.fontWeight = "bold";
    tdStatus.style.color = value.status === "OK" ? "#16a34a" : "#dc2626";
    tdStatus.style.padding = "6px 8px";
    tdStatus.style.width = "60px";
    tdStatus.style.borderBottom = "1px solid #eee";

    // Lý do
    const tdReason = document.createElement("td");
    tdReason.textContent = value.reason;
    tdReason.style.padding = "6px 8px";
    tdReason.style.borderBottom = "1px solid #eee";

    row.appendChild(tdKey);
    row.appendChild(tdStatus);
    row.appendChild(tdReason);

    table.appendChild(row);
  });

  resultBox.appendChild(table);
}

function display6SResults(objects) {
  resultBox.innerHTML = ""; // Xóa nội dung cũ

  objects.forEach(item => {
    const wrapper = document.createElement("div");
    wrapper.style.marginBottom = "12px";

    const title = document.createElement("h4");
    title.textContent = `🔹 ${item["Criteria"] || "Undefined"}`;
    title.style.marginBottom = "4px";
    title.style.color = "#1e3a8a";

    const rating = document.createElement("p");
    rating.textContent = `Evaluate: ${item["Evaluate"] || "-"}`;

    wrapper.appendChild(title);
    wrapper.appendChild(rating);

    if (item["Detail Error"]) {
      const list = document.createElement("ul");
      item["Detail Error"].forEach(err => {
        const li = document.createElement("li");
        li.innerHTML = `🛑 <b>Reason:</b> ${err["Reason"]} <br><b>Object:</b> ${err["Object Error"]}`;
        list.appendChild(li);
      });
      wrapper.appendChild(list);
    }

    resultBox.appendChild(wrapper);
  });
}

function displayECResults(values) {
  resultBox.innerHTML = "<h4>Result:</h4><ul>";

  for (const [key, value] of Object.entries(values)) {
    resultBox.innerHTML += `<li><b>${key}:</b> ${value}</li>`;
  }

  resultBox.innerHTML += "</ul>";
}

btnAnalyzeEC.addEventListener("click", async () => {
  if (capturedImages.length === 0) {
    alert("Chưa có ảnh nào để phân tích.");
    return;
  }

  loading.style.display = "block";
  resultBox.innerHTML = "";

  try {
    // Đẩy tất cả các ảnh lên
    const formData = new FormData();
    for (let i = 0; i < capturedImages.length; i++) {
      const dataUrl = capturedImages[i];
      const blob = await (await fetch(dataUrl)).blob();
      const file = new File([blob], `image_${i + 1}.jpg`, { type: "image/jpeg" });
      formData.append("files", file);
    }

    const res = await fetch("/api/v1/fire_extinguisher_cabinet/fire_extinguisher_cabinet/", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error("Phân tích tủ điện thất bại: " + res.statusText);
    }

    const result = await res.json();
    loading.style.display = "none";

    // Hiển thị kết quả (tuỳ backend trả về gì, bạn có thể tuỳ chỉnh lại hàm này)
    displayFireCabinet5SResult(result);
    previewTitle.textContent = "Result Images";

  } catch (err) {
    loading.style.display = "none";
    console.error("Lỗi phân tích tủ điện:", err);
    alert("Lỗi khi gọi API fire_extinguisher_cabinet: " + (err.message || err));
  }
});

// ...existing code...
btnAnalyze6S.addEventListener("click", async () => {
  if (capturedImages.length === 0) {
    alert("Chưa có ảnh nào để phân tích.");
    return;
  }

  loading.style.display = "block";
  resultBox.innerHTML = "";

  try {
    // Đẩy tất cả các ảnh lên
    const formData = new FormData();
    for (let i = 0; i < capturedImages.length; i++) {
      const dataUrl = capturedImages[i];
      const blob = await (await fetch(dataUrl)).blob();
      const file = new File([blob], `image_${i + 1}.jpg`, { type: "image/jpeg" });
      formData.append("files", file);
    }

    const res = await fetch("/api/v1/fire_extinguisher/cut_fire_extinguisher/", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      throw new Error("Phân tích thất bại: " + res.statusText);
    }

    const result = await res.json();
    loading.style.display = "none";

    // Hiển thị kết quả
    displayFireExtinguisherResults(result);
    previewTitle.textContent = "Result Images";

  } catch (err) {
    loading.style.display = "none";
    console.error("Lỗi phân tích:", err);
    alert("Lỗi khi gọi API cut_fire_extinguisher: " + (err.message || err));
  }
});
// ...existing code...

btnReset.addEventListener("click", () => {
  // Reset biến
  capturedImages = [];
  currentImageIndex = -1;

  // Reset preview
  updatePreview();
  previewTitle.textContent = "Captured Images";

  // Reset kết quả phân tích
  resultBox.innerHTML = "";

  // Ẩn loading nếu còn
  loading.style.display = "none";
});
