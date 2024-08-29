

# Mô tả bài toán

Diffusion limited aggregation (DLA) là một quy trình mà ở đó các hạt vật chất trải qua một quá trình bước ngẫu nhiên (random walk) tuân theo chuyển động Brownian, kết cục lại tạo thành một tập hợp. Lý thuyết này được đề xuất bởi T.A Witten Jr và L.M. Sander vào năm 1981, và có thể áp dụng vào quá trình kết tập trong một hệ thống bất kỳ mà sự khuếch tán chính là phương tiện cơ bản của quá trình di chuyển trong hệ thống. DLA có thể được quan sát trong rất nhiều quá trình tự nhiên như mạ điện, mỏ khoáng, sự cố điện môi...

Chuyển động Brownian mô phỏng chuyển động của các hạt trong môi trường chất lỏng hoặc khí, nó được coi là các quá trình ngẫu nhiên liên tục đơn giản. Quá trình chuyển động này được mô tả lần đầu tiên bởi Robert Brown khi ông quan sát các hạt phấn hoa lắc lư dưới kính hiển vi vào năm 1827. Quay trở lại, thì một cụm được tạo thành trong quy trình DLA được coi như là một cây Brownian. Cụ thể về cách hình thành cây Brownian sẽ được trình bày ở phần sau, song nói một cách ngắn gọn thì quy trình DLA bao gồm các hạt vật chất di chuyển ngẫu nhiên, hễ nó gặp phải tập hợp kết tinh, thì nó sẽ cố định tại điểm va chạm, không di chuyển nữa. Dưới đây là một hình ảnh của cây Brownian.
<p align="center">
  <img src="https://i.postimg.cc/xdPDTWC3/image.png" />
</p>

Hình dạng của cây Brownian chịu tác động của nhiều nhân tố khác nhau:

- Vị trí của hạt nhân khởi tạo
- Chiến lược khởi tạo vị trí của các hạt vật chất mới
- Chiến lược di chuyển của hạt vật chất

Mục tiêu đặt ra trong repo này là xây dựng một chương trình mô phỏng chu trình DLA, cũng như nghiên cứu sự tác động của các nhân tố tới hình dạng của cây Brownian.
