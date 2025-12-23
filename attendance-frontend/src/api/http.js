const BASE_URL = "http://127.0.0.1:8000";

export async function http(path, options = {}) {
    'ví dụ: http("/api/login", { method: "POST", body: {...} })'
    // nếu option có method thì dùng không thì dùng GET
    const method = options.method || "GET";
    // lấy dữ liệu gửi lên backend nếu có
    const bodyObj = options.body;

    const res = await fetch(BASE_URL + path, {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
        // nếu không có body thì undefine( GET không được có body)
        body: bodyObj ? JSON.stringify(bodyObj) : undefined,

    });

    // backend trả kết quả
    // backend trả thành công nhưng không có dữ liệu: http 204 = No Content => frontend nhận Null là đúng
    if (res.status === 204) {
        return null;
    }

    // Parse Json an toàn vì không phải API nào cũng trả Json ví dụ 204 => không có Json
    let data = null;
    try {
        data = await res.json();
    } catch (e) {
        data = null;
    }

    //kiểm tra http có lỗi không
    //res.ok là biến có sẵn của fetch(200,202,204 là true)
    if (!res.ok) {
        const msg = (data && (data.error || data.message))
            ? (data.error || data.message)
            : ("HTTP" + res.status)
        throw new Error(msg);
    }
    return data && data.data !== undefined ? data.data : data;
}