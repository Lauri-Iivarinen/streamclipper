
const saveClip = (url) => {
    console.log("saving clip to " + url)
    document.getElementById("loading_text").innerHTML = "SAVING VIDEO"
    window.location.href = "/save"
}
