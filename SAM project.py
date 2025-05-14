import { useState } from "react";
import { StyleSheet, Text, View, TextInput, TouchableOpacity } from "react-native";
import { PATHS } from "@/constants/pathConstants";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import { postReq } from "../../hooks/useQuery";


export default function ChangePassword() {

  
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const handleChangePassword = async () => {
    if (newPassword === "" || newPassword !== confirmPassword || oldPassword === "") {
      alert("Passwords do not match or all fields are not filled.");
      return;
    }

    try {
      const userData = {
        username: user.email,
        currentPassword: oldPassword,
        newPassword: confirmPassword,
      };
      const { data, error, isError, message } = await postReq("/user/changepassword", userData);
      if (!isError) {
        console.log(data);
        alert("Password updated successfully!");
        navigate(PATHS.SETTING);
      } else {
        console.log("Error:", message);
        alert(message);
      }
    } catch (err) {
      alert("Error updating password.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.subHeaderText}>Change Password</Text>
      <View style={styles.section}>
        <Text style={styles.label}>Old Password</Text>
        <TextInput
          style={styles.input}
          secureTextEntry={true}
          value={oldPassword}
          onChangeText={setOldPassword}
          placeholder="Enter old password"
        />
      </View>
      <View style={styles.section}>
        <Text style={styles.label}>New Password</Text>
        <TextInput
          style={styles.input}
          secureTextEntry={true}
          value={newPassword}
          onChangeText={setNewPassword}
          placeholder="Enter new password"
        />
      </View>
      <View style={styles.section}>
        <Text style={styles.label}>Re-enter New Password</Text>
        <TextInput
          style={styles.input}
          secureTextEntry={true}
          value={confirmPassword}
          onChangeText={setConfirmPassword}
          placeholder="Re-enter new password"
        />
      </View>
      <TouchableOpacity style={styles.button} onPress={handleChangePassword}>
        <Text style={styles.buttonText}>
          Save Password <FontAwesome name="save" size={20} />
        </Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    padding: 20,
  },
  subHeaderText: {
    fontSize: 20,
    fontWeight: "bold",
    marginVertical: 20,
    color: PATHS.mainColor,
  },
  section: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    marginBottom: 8,
    color: "#333",
  },
  input: {
    height: 40,
    borderColor: "#ddd",
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    backgroundColor: "#f9f9f9",
  },
  button: {
    backgroundColor: PATHS.mainColor,
    paddingVertical: 12,
    borderRadius: 5,
    alignItems: "center",
    alignSelf: "center",
    width: "40%",
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
});



import * as ImagePicker from "expo-image-picker";
import { useState } from "react";
import { StyleSheet, Text, View, TextInput, TouchableOpacity, Image, ScrollView } from "react-native";
import { useUserSessions } from "../../hooks/useUserSessions";
import { useNavigate } from "react-router-native";
import { PATHS } from "@/constants/pathConstants";

export default function UpdateProfile() {
  const navigate = useNavigate();
  const { user, isLoading, editUser } = useUserSessions();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [profileImg, setProfileImg] = useState(null);

  if (isLoading) {
    return <Text>Loading...</Text>;
  }

  if (!user) {
    navigate(PATHS.LOGIN);
    return null;
  }



  const handleUpdateProfile = async () => {
    if (!name || !email) {
      alert("Name and email cannot be empty.");
      return;
    }

    // Prepare form data to send to the server
    const formData = new FormData();
    formData.append("name", name);
    formData.append("email", email);

    // Only append the image if it's selected
    if (profileImg) {
      formData.append("profileimg", {
        uri: profileImg.uri,
        type: profileImg.type,
        name: "profile-image.jpg", 
      });
    }

    try {
      const response = await fetch( PATHS.BASEURL+"/user/updateProfile", {
        method: "POST",
        body: formData,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      const result = await response.json();

      // if (response.ok) {
      //   editUser({ name, email, profileimg: result.profileImgPath });
      //   alert("Profile updated successfully!");
      // } else {
      //   alert(Failed to update profile: ${result.message || "Unknown error"});
      // }
    } catch (error) {
      console.error("Error updating profile:", error);
      alert("There was an error updating your profile.");
    }
  };

  const updateImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== "granted") {
      alert("Permission to access media library is required!");
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 1,
    });

    if (!result.canceled) {
      setProfileImg(result.assets[0]); // Store the selected image

    }
  };

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Text style={styles.headerText}>Update Your Profile Details</Text>

        <View style={styles.section}>
          <Text style={styles.label}>Name</Text>
          <TextInput
            style={styles.input}
            value={name}
            onChangeText={setName}
            placeholder="Enter your name"
          />
        </View>
        <View style={styles.section}>
          <Text style={styles.label}>Email</Text>
          <TextInput
            style={styles.input}
            value={email}
            onChangeText={setEmail}
            placeholder="Enter your email"
          />
        </View>
        <View style={styles.section}>
          <Text style={styles.label}>Profile Image</Text>
          {profileImg ? (
            <Image source={{ uri: profileImg.uri }} style={styles.profileImage} />
          ) : (
            <Text style={styles.placeholder}>No Image Uploaded</Text>
          )}
          <TouchableOpacity
            style={[styles.button, styles.buttonMedium]}
            onPress={updateImage}
          >
            <Text style={styles.buttonText}>Upload Image</Text>
          </TouchableOpacity>
        </View>
        <TouchableOpacity
          style={[styles.button, styles.buttonWide]}
          onPress={handleUpdateProfile}
        >
          <Text style={styles.buttonText}>Save Profile</Text>
        </TouchableOpacity>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    marginBottom: 50,
  },
  scrollContent: {
    padding: 20,
  },
  headerText: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
    textAlign: "center",
    color: PATHS.mainColor,
  },
  section: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    marginBottom: 8,
    color: "#333",
  },
  input: {
    height: 40,
    borderColor: "#ddd",
    borderWidth: 1,
    borderRadius: 5,
    paddingHorizontal: 10,
    backgroundColor: "#f9f9f9",
  },
  profileImage: {
    width: 100,
    height: 100,
    borderRadius: 50,
    marginBottom: 10,
  },
  placeholder: {
    fontSize: 14,
    color: "#999",
    marginBottom: 10,
  },
  button: {
    backgroundColor: PATHS.mainColor,
    paddingVertical: 12,
    borderRadius: 5,
    alignItems: "center",
    alignSelf: "center",
  },
  buttonWide: {
    width: "60%",
  },
  buttonMedium: {
    width: "60%",
  },
  buttonText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "bold",
  },
});



import { StyleSheet, Text, Image, View, TouchableOpacity, ScrollView } from "react-native";
import { PATHS } from "@/constants/pathConstants";
import { Link } from "react-router-native";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import { useUserSessions } from "../../hooks/useUserSessions";
import { useNavigate } from "react-router-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useState, useEffect } from "react";

export default function Setiins() {
    let navigate = useNavigate();
    const { user, isLoading, editUser } = useUserSessions();

    useEffect(() => {
        if (!isLoading && !user) {
            navigate(PATHS.LOGIN);
        }
    }, [isLoading, user, navigate]);

    const [isEnabled, setIsEnabled] = useState(false);

    let logoutbtn = async () => {
        try {
            editUser(null);
            await AsyncStorage.removeItem("userSession");
            navigate("/");
        } catch (e) {
            console.log(e);
        }
    };

    return (
       
            <View style={styles.container}>
                <Link to={PATHS.PROFILE} underlayColor="#ddd">
                <View style={styles.profileInfo}>
                    <Image
                        style={styles.logo}
                        source={{
                            uri: "https://img.freepik.com/premium-vector/hipster-frofile-hat-with-glasses_6229-762.jpg",
                        }}
                    />
                    <Text style={styles.email}>{user?.email}</Text>
                </View>
                </Link>

                <TouchableOpacity>
                    <Link to={PATHS.UPDATEPROFILE} underlayColor="#ddd">
                        <View style={styles.linkContent}>
                            <Text style={styles.name}>{user?.name}</Text>
                            <FontAwesome name="edit" style={styles.edit} />
                        </View>
                    </Link>
                </TouchableOpacity>
                <TouchableOpacity>
                    <Link to={PATHS.CHANGEPASSWORD} underlayColor="#ddd">
                        <View style={styles.linkContent}>
                            <Text style={styles.name}>Change password</Text>
                            <FontAwesome name="edit" style={styles.edit} />
                        </View>
                    </Link>
                </TouchableOpacity>

                <View style={styles.linkContent}>
                <Text>Enable Notifications</Text>
                    <TouchableOpacity onPress={() => setIsEnabled(!isEnabled)}>
                        
                        <View style={styles.radio}>
                            <View
                                style={isEnabled ? styles.radioSelected : styles.radioUnselected}
                            />
                        </View>
                    </TouchableOpacity>
                </View>

                <TouchableOpacity onPress={logoutbtn} style={styles.log}>
                    <View style={styles.logout}>
                        <Text style={styles.logoutText}>Logout</Text>
                        
                    </View>
                </TouchableOpacity>
            </View>
        
    );
}

const styles = StyleSheet.create({
    container: {
        padding: 10,
        gap: 10,
    },
    profileInfo: {
        alignItems: "center",
        marginBottom: 5,
    },
    logo: {
        height: 100,
        width: 100,
        borderRadius: 50,
        marginBottom: 10,
    },
    name: {
        fontSize: 20,
        fontWeight: "normal",
    },
    email: {
        fontSize: 20,
        fontWeight: "300",
    },
    linkContent: {
        padding: 8,
        justifyContent: "space-between",
        backgroundColor: "#f0f0f0",
        borderRadius: 5,
        flexDirection: "row",
        alignItems: "center",
    },
    edit: {
        fontSize: 20,
        color: PATHS.mainColor,
        marginLeft: -10,
    },
    radio: {
        height: 20,
        width: 20,
        borderRadius: 10,
        borderWidth: 2,
        borderColor: PATHS.mainColor,
        alignItems: "center",
        justifyContent: "center",
        marginRight: 10,
    },
    radioSelected: {
        height: 10,
        width: 10,
        borderRadius: 5,
        backgroundColor: PATHS.mainColor,
    },
    radioUnselected: {
        height: 10,
        width: 10,
        borderRadius: 5,
        backgroundColor: "transparent",
    },
    logout: {
        padding: 8,
        justifyContent: "center",
        backgroundColor: "#f0f0f0",
        borderRadius: 5,
        flexDirection: "row",
        alignItems: "center",
        gap: 20,
    },
    logouti: {
        color: "red",
    },
    logoutText: {
        color: "red",
        fontSize: 20,
        fontWeight: "500",
    },
    log:{
        marginTop:320
    }
});


ksg16@05NPG