#include <iostream>
#include <boost/beast.hpp>
#include <boost/asio.hpp>
#include <string>
#include <fstream>
#include <vector>
#include <thread>
#include <stdexcept>
/**************************************************************
 * Author: Abbhinav Bharadwaj
 * Release date: 01/01/2025
 * Purpose: handles http sessions at specified port for a specific directory
 * Dependencies: Boost libraries: ASIO and Beast
 * Reason: As it always goes, C++ is the fastest. 
*/
std::string PATH;
class Error_404 : public std::exception {
public:
	const char* what() const noexcept override {
		return "Resource not found";
	}
};
class Error_400 : public std::exception {
public:
	const char* what() const noexcept override {
		return "Bad Request";
	}
};
std::string getFileExtension(const std::string& filename) {

	size_t dotPos = filename.find_last_of('.');
	if (dotPos == std::string::npos) {
		return "";
	}
	return filename.substr(dotPos + 1);
}
std::string detect_image_type(const std::string& file_path) {
	std::ifstream file(file_path, std::ios::binary);
	if (!file.is_open()) {
		throw std::runtime_error("Could not open file");
	}

	unsigned char header[8];
	file.read(reinterpret_cast<char*>(header), sizeof(header));

	if (header[0] == 0xFF && header[1] == 0xD8) {
		return "jpeg";
	}
	else if (header[0] == 0x89 && header[1] == 0x50 &&
		header[2] == 0x4E && header[3] == 0x47) {
		return "png";
	}
	else if (header[0] == 0x47 && header[1] == 0x49 &&
		header[2] == 0x46) {
		return "gif";
	}
	else if (header[0] == 0x42 && header[1] == 0x4D) {
		return "bmp";
	}
	else if (header[0] == 0x49 && header[1] == 0x49 &&
		header[2] == 0x2A && header[3] == 0x00) {
		return "tiff";
	}
	else if (header[0] == 0x4D && header[1] == 0x4D &&
		header[2] == 0x00 && header[3] == 0x2A) {
		return "tiff";
	}
	else {
		return "NULL";
	}
}
void session(boost::asio::ip::tcp::socket socket) {
	try {
		boost::beast::flat_buffer buffer;
		boost::beast::http::request<boost::beast::http::string_body> req;
		boost::beast::http::read(socket, buffer, req);
		boost::beast::string_view target = req.target();
		std::string res_path(target.data(), target.size());
		if (res_path == "/") res_path = "/index.html";
		res_path = PATH + res_path;
		std::ifstream page(res_path, std::ios::binary);
		std::cout << res_path << std::endl;
		if (!page) throw Error_404();
		std::vector<char> thread_response((std::istreambuf_iterator<char>(page)), std::istreambuf_iterator<char>());
		boost::beast::http::response<boost::beast::http::vector_body<char>> res{
			boost::beast::http::status::ok, req.version() };
		res.body() = std::move(thread_response);
		res.set(boost::beast::http::field::server, "DASH 1.0");
		{
			std::string extension = getFileExtension(res_path);	
			if (extension == "") extension = detect_image_type(res_path);
			if (extension == "html")
				res.set(boost::beast::http::field::content_type, "text/html");
			else if (extension == "css")
				res.set(boost::beast::http::field::content_type, "text/css");
			else if (extension == "js")
				res.set(boost::beast::http::field::content_type, "application/javascript");
			else if (extension == "csv")
				res.set(boost::beast::http::field::content_type, "text/csv");
			else if (extension == "json")
				res.set(boost::beast::http::field::content_type, "text/json");
			else if (extension == "xml")
				res.set(boost::beast::http::field::content_type, "text/xml");
			else if (extension == "txt")
				res.set(boost::beast::http::field::content_type, "text/plain");
			else if (extension == "png")
				res.set(boost::beast::http::field::content_type, "image/png");
			else if (extension == "jpeg" || extension == "jpg")
				res.set(boost::beast::http::field::content_type, "image/jpeg");
			else if (extension == "bmp")
				res.set(boost::beast::http::field::content_type, "image/bmp");
			else if (extension == "gif")
				res.set(boost::beast::http::field::content_type, "image/gif");
			else if (extension == "svg")
				res.set(boost::beast::http::field::content_type, "image/svg+xml");
			else if (extension == "")
				res.set(boost::beast::http::field::content_type, "image/bmp");
			else if (extension == "mp3")
				res.set(boost::beast::http::field::content_type, "audio/mpeg");
			else if (extension == "wav")
				res.set(boost::beast::http::field::content_type, "audio/wav");
			else if (extension == "webm")
				res.set(boost::beast::http::field::content_type, "audio/webm");
			else if (extension == "ogg")
				res.set(boost::beast::http::field::content_type, "audio/ogg");
			else if (extension == "mp4")
				res.set(boost::beast::http::field::content_type, "video/mp4");
			else if (extension == "ogv")
				res.set(boost::beast::http::field::content_type, "video/ogg");
			else if (extension == "webm")
				res.set(boost::beast::http::field::content_type, "video/webm");
			else if (extension == "avi")
				res.set(boost::beast::http::field::content_type, "video/avi");
			else if (extension == "mpeg" || extension == "mpg")
				res.set(boost::beast::http::field::content_type, "video/mpeg");
			else if (extension == "pdf")
				res.set(boost::beast::http::field::content_type, "application/pdf");
			else throw Error_400();
		}
		res.prepare_payload();
		boost::beast::http::write(socket, res);
		socket.shutdown(boost::asio::ip::tcp::socket::shutdown_send);
	}
	catch (const Error_404& e) {
		boost::beast::http::response<boost::beast::http::string_body> res{
		boost::beast::http::status::not_found, 11 };
		res.set(boost::beast::http::field::server, "DASH 1.0");
		res.set(boost::beast::http::field::content_type, "text/plain");
		res.body() = "Error 404: Resource not found on server.";
		res.prepare_payload();
		boost::beast::http::write(socket, res);
		socket.shutdown(boost::asio::ip::tcp::socket::shutdown_send);
	}
	catch (const Error_400& e) {
		boost::beast::http::response<boost::beast::http::string_body> res{
		boost::beast::http::status::bad_request, 11 };
		res.set(boost::beast::http::field::server, "DASH 1.0");
		res.set(boost::beast::http::field::content_type, "text/plain");
		res.body() = "Error 400: Bad Request";
		res.prepare_payload();
		boost::beast::http::write(socket, res);
		socket.shutdown(boost::asio::ip::tcp::socket::shutdown_send);
	}
	catch (const std::exception& e) {
		std::cerr << "Error: " << e.what() << std::endl;
	}
}
int main(int argc, char* argv[]) {
	/**********************************************************************
    * Uncomment the below statements while compiling this module standalone
    * Remove the arguments taken by main() viz. argc and argv 
    * Make sure boost libraries are installed properly.
    ***********************************************************************/
    //std::cout << "Please enter the absolute path of server directory:";
	//std::cin >> PATH;
	//std::cout << std::endl;
	if (argc < 3) {
		std::cerr << "Usage: " << "http.exe <server_directory> <port>" << std::endl;
		return EXIT_FAILURE;
	}
	PATH = argv[1];
	unsigned short port = std::stoi(argv[2]);
	//std::cout << "Enter Port to listen:" << std::endl;
	//std::cin >> port;
	try {
		boost::asio::io_context threads;
		boost::asio::ip::tcp::acceptor acceptor{ threads, {boost::asio::ip::tcp::v4(),port} };
		std::cout << "Server is live on port"+ std::to_string(port) << std::endl;
		std::cout << "URL: http://localhost:"+std::to_string(port)+" or device IP:"+std::to_string(port)<< std::endl;
		while (true) {
			boost::asio::ip::tcp::socket socket{ threads };
			acceptor.accept(socket);
			std::thread(&session, std::move(socket)).detach();
		}
	}
	catch (const std::exception& e) {
		std::cerr << "Fatal Error: " << e.what() << std::endl;
		return EXIT_FAILURE;
	}
	return EXIT_SUCCESS;
}
