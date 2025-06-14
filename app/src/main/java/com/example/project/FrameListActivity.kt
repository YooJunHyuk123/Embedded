package com.example.project  // 너의 패키지 이름에 맞춰줘

import android.os.Bundle
import android.util.Log
import android.widget.ImageView
import android.widget.LinearLayout
import androidx.appcompat.app.AppCompatActivity
import com.bumptech.glide.Glide
import okhttp3.*
import org.json.JSONArray
import org.json.JSONObject
import java.io.IOException

class FrameListActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_frame_list)

        val frameContainer = findViewById<LinearLayout>(R.id.frameContainer)

        // URL 목록 받아오기
        val client = OkHttpClient()
        val request = Request.Builder()
            .url("http://172.31.52.23:8123/frame_list/")
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                e.printStackTrace()
            }

            override fun onResponse(call: Call, response: Response) {
                val json = response.body?.string()
                val jsonObject = JSONObject(json)
                val frames = jsonObject.getJSONArray("frames")

                runOnUiThread {
                    for (i in 0 until frames.length()) {
                        val imageUrl = frames.getString(i)
                        val imageView = ImageView(this@FrameListActivity)
                        imageView.layoutParams = LinearLayout.LayoutParams(
                            LinearLayout.LayoutParams.MATCH_PARENT,
                            600
                        )

                        Glide.with(this@FrameListActivity)
                            .load(imageUrl)
                            .into(imageView)

                        frameContainer.addView(imageView)
                    }
                }
            }
        })
    }
}
