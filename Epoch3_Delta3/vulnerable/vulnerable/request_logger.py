import time

class RequestLoggerMiddleware(object):
    def process_request(self, request):
        # Open request log file
        f = open('requests.log', 'a')

        # Log GET requests
        if request.method == 'GET':
            f.write("------\n" + "\tTimestamp: " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n\tRemote IP: " + str(request.META['REMOTE_ADDR']) + "\n\tRemote Hostname: " + str(request.META['REMOTE_HOST']) + "\n\tFull URL: " + str(request.get_host()) + str(request.get_full_path()) + "\n\tURL path: " + str(request.get_full_path()) + "\n\tRequest method: " + str(request.method) + "\n\tRequest params: " + str(request.GET) + "\n")
            f.close()

        # Log POST requests
        if request.method == 'POST':
            f.write("------\n" + "\tTimestamp: " + str(time.strftime("%Y-%m-%d %H:%M:%S")) + "\n\tRemote IP: " + str(request.META['REMOTE_ADDR']) + "\n\tRemote Hostname: " + str(request.META['REMOTE_HOST']) + "\n\tFull URL: " + str(request.get_host()) + str(request.get_full_path()) + "\n\tURL path: " + str(request.get_full_path()) + "\n\tRequest method: " + str(request.method) + "\n\tRequest params: " + str(request.POST) + "\n")
            f.close()

        return