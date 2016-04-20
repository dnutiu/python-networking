#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>

#define SERVER_PORT 1337

int main(void) {
  struct sockaddr_in server;
  struct sockaddr_in client;
  int sock, client_len, fd;

  // Creating the socket.
  sock = socket(AF_INET, SOCK_STREAM, 0);

  // Setting local address.
  server.sin_family      = AF_INET;
  server.sin_addr.s_addr = htonl(INADDR_ANY);
  server.sin_port        = htons(SERVER_PORT);

  bind(sock, (struct sockaddr *) &server, sizeof(server));

  // Waiting for business.
  printf("Server started.\n");
  listen(sock, 5);
  client_len = sizeof(client);
  fd = accept(sock, (struct sockaddr *) &client, (socklen_t *) &client_len);
  printf("Got client\n");

  // Talking to the client.
  unsigned char buf[1024];
  int count;
  while ( (count = read(fd, buf, 1024)) > 0 ) {
    printf("Client wrote: %s\n", buf);
    write(fd, "Echo: ", 6);
    write(fd, buf, count);
  }

  return 0;
}
