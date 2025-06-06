<div class="flex items-center justify-center h-screen w-full">
  <div class="flex flex-col bg-gray-300 rounded-3xl gap-2 items-center justify-center w-full py-8 md:w-1/3">
    <h1 class="text-2xl font-bold mb-4">Login</h1>
    <form method="POST" class="flex flex-col gap-2">
      <div class="flex gap-2 items-center">
        <label for="username" class="text-lg font-semibold min-w-24">Username</label>
        <input 
          class="bg-white px-4 py-2 rounded-full"
          name="username" 
          placeholder="Enter user name..."
        />
      </div>
      <div class="flex gap-2 items-center">
        <label for="password" class="text-lg font-semibold min-w-24">Password</label>
        <input 
          class="bg-white px-4 py-2 rounded-full"
          type="password"
          name="password" 
          placeholder="Enter password..."
        />
      </div>
      <button class="bg-blue-300 p-2 rounded-full cursor-pointer mt-8" type="submit">Submit</button>
    </form>
  </div>
</div>
