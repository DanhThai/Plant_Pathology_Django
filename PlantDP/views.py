from django.shortcuts import render

from PlantDP.models import Disease, Pesticide, Plant

# Create your views here.

def Home(request):
    plant = Plant(name ="Cây táo")
    disease = Disease(
            name = "Bệnh nấm táo",
            cause = "Do nấm Guignardia bidwellii gây ra. Là một bệnh nghiêm trọng đối với nho trồng và nho dại. Bệnh phá hoại mạnh nhất vào mùa ấm, ẩm ướt. Nó tấn công tất cả các phần xanh của cây nho, lá, chồi, thân lá và quả, gân và quả. Tác hại nặng nề nhất là đối với quả. Lưu ý: Guignardia bidwellii forma parthenocissi gây ra đốm lá trên cây thường xuân Boston và cây leo Virginia.",
            symptom = "Các đốm màu nâu đỏ và hình tròn đến góc cạnh xuất hiện ở mặt trên của lá bắt đầu từ cuối mùa xuân. Khi các đốm hợp nhất, chúng tạo thành các đốm màu nâu đỏ không đều. Số lượng đốm hoặc vết bệnh trên mỗi lá thay đổi từ 2 đến hơn 100 tùy theo mức độ nghiêm trọng của bệnh. Trung tâm của đốm lá chuyển sang màu nâu nhạt và được bao quanh bởi một viền đen. Quả thể màu đen, kích thước bằng hạt bụi (pycnidia) được sắp xếp thành một vòng xác định ngay bên trong rìa của vết bệnh.",
            precautions = "Chọn một vị trí trồng nơi dây leo sẽ được tiếp xúc với ánh nắng mặt trời đầy đủ và lưu thông không khí tốt.\n Giữ cho khu vực trồng cây ăn quả và các khu vực xung quanh không có cỏ dại và cỏ cao.\n Cắt tỉa dây leo vào đầu mùa đông trong thời gian ngủ đông.\n Sử dụng thuốc xịt bảo vệ nấm.",
            status = False,
            plant = plant
        )
    context = {
        "disease": disease
    }
    return render(request, 'home.html', context)

def Diseases(request):
    diseases = []
    plant = Plant(name ="Cây táo")
    for i in range(10):
        disease = Disease(
            id = i,
            name = "Bệnh nấm táo",
            cause = "Do nấm Guignardia bidwellii gây ra. Là một bệnh nghiêm trọng đối với nho trồng và nho dại. ",      
            plant = plant
        )
        diseases.append(disease)
    context = {
        "diseases" : diseases
    }
    return render(request, 'diseases.html', context)

def DiseaseDetail(request, id):
    plant = Plant(name ="Cây táo")
    disease = Disease(
        id = 0,
        name = "Bệnh nấm táo",
        cause = "Do nấm Guignardia bidwellii gây ra. Là một bệnh nghiêm trọng đối với nho trồng và nho dại. Bệnh phá hoại mạnh nhất vào mùa ấm, ẩm ướt. Nó tấn công tất cả các phần xanh của cây nho, lá, chồi, thân lá và quả, gân và quả. Tác hại nặng nề nhất là đối với quả. Lưu ý: Guignardia bidwellii forma parthenocissi gây ra đốm lá trên cây thường xuân Boston và cây leo Virginia.",
        symptom = "Các đốm màu nâu đỏ và hình tròn đến góc cạnh xuất hiện ở mặt trên của lá bắt đầu từ cuối mùa xuân. Khi các đốm hợp nhất, chúng tạo thành các đốm màu nâu đỏ không đều. Số lượng đốm hoặc vết bệnh trên mỗi lá thay đổi từ 2 đến hơn 100 tùy theo mức độ nghiêm trọng của bệnh. Trung tâm của đốm lá chuyển sang màu nâu nhạt và được bao quanh bởi một viền đen. Quả thể màu đen, kích thước bằng hạt bụi (pycnidia) được sắp xếp thành một vòng xác định ngay bên trong rìa của vết bệnh.",
        precautions = "- Chọn một vị trí trồng nơi dây leo sẽ được tiếp xúc với ánh nắng mặt trời đầy đủ và lưu thông không khí tốt.\n - Giữ cho khu vực trồng cây ăn quả và các khu vực xung quanh không có cỏ dại và cỏ cao.\n - Cắt tỉa dây leo vào đầu mùa đông trong thời gian ngủ đông.\n - Sử dụng thuốc xịt bảo vệ nấm.",
        status = False,
        plant = plant
    )
    context = {
        "disease" : disease
    }
    return render(request, 'disease-detail.html', context)


def Pesticides(request):
    pesticides = []
    for i in range(8):
        pesticide = Pesticide(
            id = i,
            name = "Xử lý tuyến trùng trong đất – AT Padave 1kg",
            producer = "Công ty nông sản VN",
            quantity = 100,
            price = 170000
        )
        pesticides.append(pesticide)
    context = {
        "pesticides" : pesticides
    }
    return render(request, 'pesticides.html', context)

def PesticideDetail(request, id):
    pesticide = Pesticide(
        name = "Xử lý tuyến trùng trong đất – AT Padave 1kg",
        producer = "Công ty nông sản VN",
        description = 
        """
            - Hoạt chất (A.I): Spinetoram.\n
            - Đặc trị: bọ trĩ và sâu khó trị.\n
            - Chiết xuất rất độc đáo từ thiên nhiên qua quy trình lên men và bán tổng hợp hiện đại nhất.\n
            - Thế hệ thuốc trừ sâu tiên tiến nhất hiện nay, an toàn và thân thiện với môi trường. Hiệu lực nhanh, kéo dài.\n
            - Thuốc có cơ chế tác động khác với thuốc khác nên diệt trừ được các loại sâu hại khó trị và kháng thuốc.\n
            - Cơ chế: Thuốc tác động lên tế bào thần kinh sâu hại tại 2 vị trí khác nhau, sâu ngừng ăn tê liệt và chết nhanh.\n
        """,
        quantity = 100,
        price = 170000
    )
    pesticides = []
    for i in range(8):
        pesticide_item = Pesticide(
            id = i,
            name = "Xử lý tuyến trùng trong đất – AT Padave 1kg",
            producer = "Công ty nông sản VN",
            quantity = 100,
            price = 170000
        )
        pesticides.append(pesticide_item)
    context = {
        "pesticides" : pesticides
    }
    context = {
        "pesticide" : pesticide,
        "pesticides" : pesticides

    }
    return render(request, 'pesticide-detail.html', context)
