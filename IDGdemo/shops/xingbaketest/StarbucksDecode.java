/*
 * Copyright (c) 2019. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
 * Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
 * Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
 * Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
 * Vestibulum commodo. Ut rhoncus gravida arcu.
 */

package xingbaketest;

import okhttp3.HttpUrl;
import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.Response;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.security.*;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Base64;

public class StarbucksDecode implements Interceptor {
    protected static String R6 ="MIIEowIBAAKCAQEA4VoHujAt31BlzIbCyNXDYEVt5F03WMEdkQ+i0RPu0YzrLUP0VGZL7R/gY3ZqDrzUau4+nDjIZ3qOyUxX2SUiL4XNgoR/0ux9KUnl8HjNmPMfFStYfDttSQYm1LwFxRaET8o+X7fM4u5UhfzR9FXJZJ8l0AIPvVAp7qgjQ0NBoLWMNFDVPJkrChw7fPuogw8lroWflBEpP6+QqTRD58+tj9C17h2cFXMpuV2aRBXsNLIg6TzoQg/fgA0nth8k25Z/npv7HMO29oOJ2tbpZltXY/2WLI407Cf8UG1dKP68M986OkwwjtPpv6jEHVoZizE/+zj4qTy7uu78lsaqppb32wIDAQABAoIBAQCzdf4XYUz2vVEEiwFN7SY1YbU9Gpr7/HauUhRoioYyrRWQq8BFAl5OzYblzqRxbiF/spF72aCG/8v8NOb0z6Sk0dqyqRAeiiS2n9oVIi8hMeQ7+JP0A2NptxNvcPjrVp4x6K65jWcGBaScO5V8DmFe13rGZw3fxppOK+pBI6t87fifUuiNNzdgqUOIXAx4kypYBAzCPuVH2ypxMxYnhnIrZ9iZcayYbF2mrYax4YGwMckGs4uFzOPiJHj6vg4cEL4g3b1vOrDgY1wwnmTM93HNqS89WYVOpFDnOTRsOlmL6COJH2U/YqHe3CbYxGXJnYjLqKJ/k5QwXaZoK+98wUnJAoGBAPhaqIh++o93gF7vicsboHT0l5DvqCPSwdwFBlr2i3ODuVLrUvHbrRDN0bTlWwO2GuEBZyXGqNGerMaJlr67BTXIg4KDwXCpMJ8YxyRUQ7EGsLp3WS6Zzt6VeSKYRMzu7CHfyUzXwK0e5kylVWeiclzFEBWHpGC5FsYRoSYNSU6/AoGBAOhKFW2b4PhjCBDzQZrUWd0lR7aGufyHaKUEVKS5isXXmOonWQT4BEsLcXX1m9i3ZN0gB4uCY+bdiLkdoEwPppSRG0e7z0a0MRB6YtC5LBhkUcYKIS41dYsOeNG2cAG2Cs3UZwHgnyC9g1NFFoCkhkV1fyRWi32c2GQCsJzIRTnlAoGADIVFidwc9a6ooiChacPyyvKp0XzDlUrCyzzVnTBgx2oUpcGHZPoWN4qoz93gQMelg0J22MizKh49x6SYHPWAxb1eI+5QikV9VggBwisdXodf0YbC0D6g10fh24Shs1M4RFzr4Rvfctrj8WlEbP0bluG4dd1oxBeQtludLDXvRDECgYAdHuyAyUHy4bdpKJXY6zY42yuaXlmCpxcfWOOjov8avmSVNkmard0b61tWBmx7RsKGVjWb78TGdI9nZadq4atohKh+3bSmkIB2KGGq+QvmIu19fleai2ko/a932v8/t6qzEyW2voo0eI22KrsfdYC/xHMkAxWJsdgO8adigFjtYQKBgGlEJcXfOKNICdKsN0/v5LSop8ZC20mO1bBHNZu8vk37/6peAH1geICS6BKfooNChavn6dfBi+ch2W19Jq73/nuYj1wdvVzkpXBmjnTLig7XBa4iOs1z/we1l+oBXf/zjg8wbptx/02mBuay6Zt3k9Pk8NjmlmqMeYje4Y+mbcg9";
    private static String SIGNATURE_ALGORITHM = "SHA256withRSA";
    protected static PrivateKey privateKey;

    static {
        PKCS8EncodedKeySpec r8 = new PKCS8EncodedKeySpec(Base64.getDecoder().decode(R6));
        KeyFactory r7 = null;
        Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());
        try {
            r7 = KeyFactory.getInstance("RSA","BC");
            privateKey = r7.generatePrivate(r8);
        } catch (NoSuchAlgorithmException e) {
            e.printStackTrace();
        } catch (InvalidKeySpecException e) {
            e.printStackTrace();
        } catch (NoSuchProviderException e) {
            e.printStackTrace();
        }

    }
    public static void main(String[] args) throws SignatureException, NoSuchAlgorithmException, InvalidKeyException, UnsupportedEncodingException {
        String str="appid=859977c6f22b4f9ce98d4b02d031b4a8&lang=zh-cn&store_id=25023";
        String output=signSha256WithRSA(str);
        System.out.println(output);
    }

    public final static String signSha256WithRSA(String str) throws NoSuchAlgorithmException, InvalidKeyException, UnsupportedEncodingException, SignatureException {
        Signature instance = Signature.getInstance(SIGNATURE_ALGORITHM);
        instance.initSign(privateKey);
        instance.update(str.getBytes("utf-8"));
        byte[] sign = instance.sign();
        String encodeString = Base64.getEncoder().encodeToString(sign);
        return encodeString;
    }

    @Override
    public Response intercept(Chain chain) throws IOException {
        Request r10 = chain.request();
        HttpUrl r11 = r10.url();
        String r13 = r10.method();
        if ("GET".equals(r13)) {
        } else if ("POST".equals(r13)) {
        }
        return null;
    }
}
