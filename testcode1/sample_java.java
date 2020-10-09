  private String encodeServerSide() {
    if (cookies.size() > 1) {
      throw new IllegalStateException(
          "encode() can encode only one cookie on server mode: " + cookies.size() + " cookies added");
    }

    Cookie cookie = cookies.isEmpty() ? null : cookies.iterator().next(); //SS
    ServerCookieEncoder encoder = strict ? ServerCookieEncoder.STRICT : ServerCookieEncoder.LAX;
    return encoder.encode(cookie);
  }
