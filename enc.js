function _private_key() {
    var i = KEYUTIL.generateKeypair("EC", "secp256r1")
                  , s = i.prvKeyObj
                  , a = i.pubKeyObj;
    // console.log(s)
    _public_key1 = KEYUTIL.getPEM(a)
     private_key1 = KEYUTIL.getPEM(s, "PKCS8PRV");
    return [_public_key1,private_key1]
}
//bd_ticket_guard_client_data生成方法
//在登录过程中会出现两个bd_ticket_guard_client_data，可以抓包base64解码查看两个bd_ticket_guard_client_data组成，
//第一个'{"bd-ticket-guard-version":2,"bd-ticket-guard-iteration-version":1,"bd-ticket-guard-ree-public-key":"BN5YmS3JDO+9bge5r1NgWzg6k6TeHcNIagDxeD77Q9rabrX+kibN38mziGVe6Jj88U2d4Zuz46Z61GjFM4NCCAc=","bd-ticket-guard-web-version":1}'
//第二个'{"ts_sign":"ts.1.3d16f1bea8bee4c5281219d3eb8dab3b56382db58c615529d1d05db8319e2b88c4fbe87d2319cf05318624ceda14911ca406dedbebeddb2e30fce8d4fa02575d","req_content":"ticket,path,timestamp","req_sign":"MEUCIBF5BF/25saHMGOOeB0I7qDRhck9ARwsFWzmMpkBzT8qAiEAoySCd7X7Sf93wRrGrLa0hCskVoF7hdBUf9WTCrd0p1s=","timestamp":1715141907}'
//我们最终需要第二个
//第一个需要解决的参数是bd-ticket-guard-ree-public-key
// 第一次是调用_private_key函数生成私钥跟公钥，调用xt函数加密私钥得到bd_ticket_guard_ree_public_key
//之后base64编码即可得到最初的bd_ticket_guard_client_data
//第二个需要解决的参数是ts_sign,req_sign
//经过一系列流程请求最终请求到一个关键请求https://www.douyin.com/passport/sso/login/callback/?ticket=你的&next=https%3A%2F%2Fwww.douyin.com
//cookie里携带第一个bd_ticket_guard_client_data请求这个关键请求响应头里即可返回bd_ticket_guard_server_data这个关键参数还有其他cookie相关的参数，base64解码后得到
//'{"ticket":"8fce9fb22205b0c2e7e43114b3523b60","ts_sign":"ts.1.3d16f1bea8bee4c5281219d3eb8dab3b56382db58c615529d1d05db8319e2b88c4fbe87d2319cf05318624ceda14911ca406dedbebeddb2e30fce8d4fa02575d","client_cert":"pub.BN5YmS3JDO+9bge5r1NgWzg6k6TeHcNIagDxeD77Q9rabrX+kibN38mziGVe6Jj88U2d4Zuz46Z61GjFM4NCCAc="}'
//这里可以得到生成最终bd_ticket_guard_client_data需要的ts_sign
//剩下req_sign待解决
//req_sign =调用js里的函数req_sign函数传入这段'ticket=' + ticket + '&path=/passport/token/beat/web/&timestamp=1715141907'和私钥privatekey
//最终加密生成出req_sign,到此bd_ticket_guard_client_data需要解决的ts_sign,req_sign都已解决
//'{"ts_sign":"","req_content":"ticket,path,timestamp","req_sign":"","timestamp":1715141907}'
//最后base64编码即可得到最终的bd_ticket_guard_client_data
